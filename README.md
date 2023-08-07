# Resonant pNN  
XtoYH pNN framework, forked from https://github.com/MatthewDKnight/ResonantGGTT. Credits to Matthew Knight (@MatthewDKnight).
  
## Instructions  
### 1. Clone this repository  

### 2. Install dependencies  
    
```  
source make_env.sh 
```  
Then activate the environment and setup the python modules with
```
source setup.sh 
```
### 3. Add extra features and mass labels  

The choice of the pNN input variables is determined by running BDTs for different signal masspoints and taking the union of the N most important variables of all them. The following exercise is designed and optimized for the resonant XtoY(gg)H(TauTau) analysis and will be updated when the pNN will be converted to run on XtoY(gg)H(bb) inputs. The starting point of this exercise are the parquet file Sam produced:
```
indir=/ceph/cms/store/user/smay/Higg```sDNA/hh_ggtautau_resonant_presel_XYH_Ygg_HTauTau_19Jul2022/
cd $indir
files=$(echo merged_*.parquet)
cd -
```  
The `*` is there to also process the dataframes with the systematic variations.

**Run input preprocessing**
``` 
for file in $files ; do
  python processInputs/process_HiggsDNA_Inputs.py -i ${indir}/$file -o <outdir>/$file -s ${indir}/summary.json -f important_17_corr_no_mggtau ;
done
```  
Typically the `summary.json` file lives in the same path as the HiggsDNA output. The -f option selects the list of input features (from [`common.py`](https://github.com/cmstas/XtoYH_pNN/blob/main/common.py#L69-L81)) that need to be added and will be considered in the pNN training.
Latest summary used, containing DDGJets is: ```/ceph/cms/store/user/azecchin/pNN/ggbb-inputs/looper/DDGjets_summary.json```

### 4. Plot input features
Not necessary, but you might want to take a look at how signals and background look like
```
python plotting/plot_input_features.py -i <outdir>/merged_nominal.parquet -s ${indir}/summary.json> -p <space-separated list of signals> -o <outdir>/inputFeatures --norm (--no-legend)
```
The list of signals can be found in [`common.py`](https://github.com/cmstas/XtoYH_pNN/blob/main/common.py#L36-L42).

### 5. Hyperparameter tuning

```
python training/train_model.py -i <outdir>/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/hpTuning -p $(cat proc_lists/Graviton.txt) --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams-grid hp/Graviton_grid.json --only-ROC
```
The above command finds the best hyperparameter set out of all combinations in the grid of `hp/Graviton_grid.json`. The training is performed on the signal samples included in `proc_lists/Graviton.txt`. The `--remove-gjets` option is to avoid using low stat gjets samples in training.

### 6. Training the pNN
```
python training/train_model.py -i <outdir>/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/trained/ -p $(cat proc_lists/Graviton.txt) --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams hp/Graviton.json --outputName merged_nominal.parquet --outputModel <outdir>/trained/model.pkl
```
The specific hyperparameters can be choosen from the one available in the hp folder. In the future one could run an optimisation of the HP once we move towards ggbb based features.

#### 6.1 current input and training features
The current input parquet files containing the DDGJets estimation and not applying the HLT bit in MC + containing the 2 extra mass variables that were looking promising from Joshua preliminary results are here ```/ceph/cms/store/user/azecchin/pNN/ggbb-inputs/looper/DDGJets_noHLTbit_newMXaggr_merged_nominal.parquet``` 

If you want to include them in the training use this features lists:
``` important_22_corr_bbgg_newMX``` or ```important_22_corr_bbgg_newMXaggr```

Baseline feature list for training is ```important_22_corr_bbgg_noMX```

#### 6.2 extra options for training

**saving the model**

```
--outputModel
--outputTransformCDFs
```
These to options have to be used together to save the pNN model and the score transformation pdfs in the output folder (they take a folder as argument, e.g. ```--outputModel <out-dir> --outputTransformCDFs <out-dir>/cdfs```). This is useful to re-evaluate the pNN scores on different inputs or rerunning the score plots , without retraining the pNN.

**loading a previously trained model**

```
--loadModel
--loadTransformCDFs
```

If you want to load the pNN and run only the steps after the training, use this 2 options, providing the path for the model and the score transformation pdfs

**skipping plots**

To speed up the training process, or if you are using  a model to score new dataframes you might want to skip part of plots that are produced by default
```
---skipPlots
```
Use this option to avoid plotting the score distributions (both raw score and transformed).

```
--skipROC
```
Use this option to avoid plotting the ROC plots

**saving all the training features in the output parquet file**

```
--keepAllFeatures
```
By default the output DF contains only the variables needed for flashggFinalFit, i.e. the diphoton mass and the systematic variations. If you want to take a look at the distributions of different training features for different pNN scores, you can use this option and the list of training features will also be saved in the scored parquet file.

#### 6.3 plotting scored dataframes

To plot the diphoton mass distribution, or all the training variables if saved in the scored dataframe, one can use the ```assess.py``` script from the HiggsDNA/bonus repository.
In paricular this [`branch`](https://gitlab.cern.ch/azecchin/HiggsDNA/-/tree/tthh_topic_dd_gjets) contains a updates that can help producing SR-like plots.
```assess.py``` takes as mandatory arguments the location of a scored dataframe, (the name of the DF should contained 'merged_nominal' to not be considered a systematic alternative collection), a ```summary.json``` as all the commands described so far  options are:

### 7. Parametric tests
```
python training/train_model.py -i <outdir>/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/paramTests -p $(cat proc_lists/Graviton.txt) --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams hp/Graviton.json --only-ROC --do-param-tests
```
The parametric tests consist in the comparison of the neural network performance when it is trained on the all the mass points, on a specific mass point or on all but one mass points. The results of the comparison can be evaluated and visualized by running:
```
python training/gather_param_tests.py -o <outdir>/paramTests --bkgEff 0.01
python plotting/plot_param_tests.py <outdir>/paramTests
```
The `bkgEff` option defines the background efficiency at which the neural network performance is to be compared.

### 8. M(gg) sculpting
```
python misc/mgg_sculpting2.py -i <outdir>/trained/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/mggSculpting
```
This script attempts to quantify the bias involved with using only a powerlaw for the description of the falling background distribution. However, the bias changes depending on the shape of the background which can change at different cuts in the score, so the method is not very reliable.

### 9. Category optimization
```
python optimisation/optimise_procedure.py -i <outdir>/trained/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/CatOptim -p $(cat proc_lists/Graviton.txt) --score intermediate_transformed_score -n 20 --n-proc-improve 2
```
This returns the optimal boundaries for the SR categories. Starting by identifying the `intermediate_transformed_score` value (controlled by the `score` option) for which there are `n` events in the sideband (controlled by the `n` option, equal to 20 in this case), the script computes the limits. Then, it proceeds to iteratively create another category with `n` more events in the sideband. If the limit is improved (more than 0.01 by default, controlled by the `frac-improve` option) for more than 2 signal processes (controlled by the `n-proc-improve` option), the new boundaries are kept, otherwise `n` is set to `2*n` and the procedure continues until there are no more events in the sideband.

### 10. Limit granularity
```
python optimisation/limit_granularity.py -i <outdir>/trained/merged_nominal.parquet -s ${indir}/summary.json -o <outdir>/LimitGranularity -p $(cat proc_lists/Graviton.txt) -r <outdir>/CatOptim/optim_results.json
```
With this command, the extra masses (those for which we have no MC) are determined. This is done by computing the relative change in the limit between a "central" mass point and its five "neighboring" ones, where the limit for the "central" mass points is computed using the score and the optimal categories of the "neighboring" ones. An extra mass point is inserted every time that the difference between a "central" mass point and its closest neighbors is larger than `0.1` (controlled by the `max-loss` option).

### 11. Retraining the pNN with the extra masses
First, keep the output with the pNN trained only on the nominal masses:
```
mv <outdir>/trained/merged_nominal.parquet <outdir>/trained/LimitGranularity/merged_nominal_only_nominal_mass_points.parquet
```
Then, retrain including the score computed on the extra masses:
```
python training/train_model.py -i <outdir>/merged_nominal.parquet -s <outdir>/summary.json -o <outdir>/trained -p $(cat proc_lists/Graviton.txt) --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams hp/Graviton.json --outputName merged_nominal.parquet --loadModel <outdir>/trained/model.pkl --skipPlots --extra-masses <outdir>/LimitGranularity/extra_masses_0p1.json
```

### 12. Category reoptimization with the extra masses
```
python optimisation/optimise_procedure.py -i <outdir>/trained/merged_nominal.parquet -s <outdir>/summary.json -o <outdir>/trained/CatOptim -p $(cat proc_lists/Graviton.txt) --score intermediate_transformed_score -n 20 --n-proc-improve 2
```

### 13. Signal modelling
```
python signalModelling/interpolate.py -i <outdir>/trained/merged_nominal.parquet -s <outdir>/summary.json -r <outdir>/CatOptim/optim_results.json -o <outdir>/Interpolation --make-plots (--interp-checks)
python plotting/plot_interpolation_uncert.py <outdir>/Interpolation/model.json <outdir>/Interpolation_Uncert
```
The normalization and shape parameters of all nominal mass points are computed and these values are interpolated for the extra mass points. This is done by using the linear or cubic spline with the lowest error for the normalization, keeping the one with the lowest error, and by using the parameters of the closest mass point for the shape. It is worth noting that the mass value for the maximum and the width of the signal shape are also interpolated with linear splines.

The `interp-checks` option verifies the interpolation procedure for the nominal mass points, while the second command produces diagnostic plots about the signal efficiency based on the different interpolations.

### 14. Systematics
```
parquets="merged_fnuf_down.parquet merged_fnuf_up.parquet merged_JER_down.parquet merged_JER_up.parquet merged_JES_down.parquet merged_JES_up.parquet merged_material_down.parquet merged_material_up.parquet merged_MET_JER_down.parquet merged_MET_JER_up.parquet merged_MET_JES_down.parquet merged_MET_JES_up.parquet merged_MET_Unclustered_down.parquet merged_MET_Unclustered_up.parquet merged_Muon_pt_down.parquet merged_Muon_pt_up.parquet merged_scale_down.parquet merged_scale_up.parquet merged_smear_down.parquet merged_smear_up.parquet merged_Tau_pt_down.parquet merged_Tau_pt_up.parquet"
for input in $parquets ; do
  python training/train_model.py -i <outdir>/$input -s <outdir>/summary.json -o <outdir>/trained -p $(cat proc_lists/Graviton.txt) --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams hp/Graviton.json --outputName $input --loadModel <outdir>/trained/Graviton/model.pkl --skipPlots --parquetSystematic --loadTransformBkg <outdir>/trained/merged_nominal.parquet;
done
python signalModelling/systematics.py -i <outdir>/trained -r <outdir>/trained/CatOptim/ -s <outdir>/summary.json -o <outdir>/Interpolation
```
Passing the systematics through the NN, evaluate their effect and save it under `<outdir>/Interpolation/systematics.json`.

### 15. Output results
```
python optimisation/tag_to_finalfits.py -i <outdir>/trained/merged_nominal.parquet -r <outdir>/trained/CatOptim/optim_results.json -s <outdir>/summary.json -o <outdir>/trained --combineYears
```
Writing out output trees and yields in `<outdir>/trained/{outputTrees,yieldTables}` respectively.

### 16. Resonant background modelling
```
python signalModelling/resonant_bkg.py -i Outputs/Graviton/ -r Outputs/Graviton/CatOptim/optim_results.json -s Inputs_Graviton/summary.json -o Outputs/Graviton/ResonantBkg --systematics --make-plots
```
With the above command, all resonant backgrounds are modelled, very simalarly to the signal modelling, if they contribute "enough", i.e. more than 0.1 events.

## Things to do
Run on ggbb signals:
 - Modify the preprocessing to produce ggbb specific variables
 - Optimise training feature selection
 - Implement ggbb available improvements (bjet regression)

Coding wise:
- import condor submission functionalities 

