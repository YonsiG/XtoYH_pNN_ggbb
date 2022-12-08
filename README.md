# Resonant pNN  
XtoYH pNN framework, forked from https://github.com/MatthewDKnight/ResonantGGTT. Credits to Matthew Knight (@MatthewDKnight).
  
## Instructions  
**1. Clone this repository**  

**2. Install dependencies**  
    
```  
source make_env.sh 
```  
Then activate the environment and setup the python modules with
```
source setup.sh 
```
**3. Add extra features and mass lables**  
  
Run input preprocessing
```  
python processInputs/process_HiggsDNA_Inputs.py -i <inputParquetfile> -o <outputParquetfile> -s <path/summary.json> -f important_17_corr_no_mggtau 
```  
The -f options select the list of input features that need to be added and will be considered in the pNN training.

**4. Plot input features**
Not necessary, but you might want to take a look at how signals and background look like
```
python plotting/plot_input_features.py -i <InputParquet> -s <path/summary.json> -p <spave separated list of signals> -o <Output_dir> --norm (--no-legend)
```

**5. Training the pNN**
```
python training/train_model.py -i <InputParquet> -s <path/summary.json> -o <Output_dir> -p <proc_lists> --train-features important_17_corr_no_mggtau --model ParamNN --outputOnlyTest --remove-gjets --hyperparams hp/<analysisSpecificHP>.json --outputName merged_nominal.parquet --outputModel <Output_dir>/model.pkl
```

--remove-gjets option is to avoid using low stat gjets samples in training, the specific hyperparameters can be choosen from the one available in the hp folder. In the future one could run an optimisation of the HP once we move towards ggbb based features.

## Things to do
Run on ggbb signals:
 - Modify the preprocessing to produce ggbb specific variables
 - Optimise training feature selection
 - Implement ggbb available improvements (bjet regression)

Coding wise:
- import condor submission functionalities 
