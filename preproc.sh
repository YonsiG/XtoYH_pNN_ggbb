indir=/ceph/cms/store/user/smay/HiggsDNA/hh_ggtautau_resonant_presel_XYH_Ygg_HTauTau_19Jul2022
outdir=/ceph/cms/store/user/azecchin/pNN/ggtt-inputs

pushd $indir
  files=$(echo *.parquet)
popd

for file in $files ; do
	echo $file
	python processInputs/process_HiggsDNA_Inputs.py -i ${indir}/$file -o ${outdir}/$file -s ${indir}/summary.json -f important_17_corr_no_mggtau 
done

cp ${indir}/summary.json ${outdir}/summary.json
