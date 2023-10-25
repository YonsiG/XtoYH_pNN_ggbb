import pandas as pd
import pyarrow.parquet as pq

pf = pq.ParquetFile("/home/users/azecchin/Analysis/ResonantGGTT/Outputs/XtoYH_ggbb_DDGJets_noHLTbit_noMX/merged_nominal_scored.parquet")

newFile=True
for i in pf.iter_batches(columns=["event", "y", "Diphoton_mass", "weight", "year", "process_id","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_320_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_450_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_450_MY_300","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_600_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_650_MY_500","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_700_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_700_MY_550","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_750_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_800_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_900_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_900_MY_700","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_950_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_950_MY_800","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_280_MY_70","intermediate_transformed_score_NMSSM_XYH_Y_gg_H_bb_MX_280_MY_150"]):
  itmp = i.to_pandas()
  itmp = itmp[(itmp["process_id"]<100) | (itmp["process_id"]==411) | (itmp["process_id"]==711) | (itmp["process_id"]==720) | (itmp["process_id"]==1011) | (itmp["process_id"]==1124) | (itmp["process_id"]==1211) | (itmp["process_id"]==1225) | (itmp["process_id"]==1311) | (itmp["process_id"]==1411) | (itmp["process_id"]==1611) | (itmp["process_id"]==1628) | (itmp["process_id"]==1711) | (itmp["process_id"]==1729) | (itmp["process_id"]==211) | (itmp["process_id"]==216)]
  if newFile:
    inew = itmp
    newFile=False
  else:
    inew = pd.concat([inew,itmp], ignore_index=True)
    
inew.to_parquet("merged_nominal_scored_skimmed.parquet")
