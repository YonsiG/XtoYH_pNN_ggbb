import pandas as pd
import argparse
import numpy as np
import json
import common
import mass_variables
import sys

dphi = lambda x, y: abs(x-y) - 2*(abs(x-y) - np.pi) * (abs(x-y) // np.pi)

def add_Deltas(df):
  df["Diphoton_deta"] = df.LeadPhoton_eta-df.SubleadPhoton_eta
  df["Diphoton_dPhi"] = dphi(df.LeadPhoton_phi,df.SubleadPhoton_phi)
  df["Diphoton_dR"] = np.sqrt( dphi(df.LeadPhoton_phi, df.SubleadPhoton_phi)**2 + (df.LeadPhoton_eta-df.SubleadPhoton_eta)**2 )

  df["dijet_deta"] = df.dijet_lead_eta - df.dijet_sublead_eta
  df["dijet_dphi"] = dphi(df.dijet_lead_phi,df.dijet_sublead_phi)
#   df.loc[df.category==8, "dijet_deta"] = common.dummy_val
#   df.loc[df.category==8, "dijet_dphi"] = common.dummy_val

  df["Diphoton_dijet_lead_deta"] = df.Diphoton_eta-df.dijet_lead_eta
  df["Diphoton_dijet_lead_dphi"] = dphi(df.Diphoton_phi,df.dijet_lead_phi)
  df["Diphoton_dijet_lead_dR"] = np.sqrt( dphi(df.Diphoton_phi,df.dijet_lead_phi)**2 + (df.Diphoton_eta-df.dijet_lead_eta)**2 )

  df["Diphoton_dijet_sublead_deta"] = df.Diphoton_eta-df.dijet_sublead_eta
  df["Diphoton_dijet_sublead_dphi"] = dphi(df.Diphoton_phi,df.dijet_sublead_phi)
  df["Diphoton_dijet_sublead_dR"] = np.sqrt( dphi(df.Diphoton_phi,df.dijet_sublead_phi)**2 + (df.Diphoton_eta-df.dijet_sublead_eta)**2 )
#   df.loc[df.category==8, "Diphoton_dijet_sublead_deta"] = common.dummy_val
#   df.loc[df.category==8, "Diphoton_dijet_sublead_dphi"] = common.dummy_val
#   df.loc[df.category==8, "Diphoton_dijet_sublead_dR"] = common.dummy_val

  df["Diphoton_dijet_deta"] = df.Diphoton_eta-df.dijet_eta
  df["Diphoton_dijet_dphi"] = dphi(df.Diphoton_phi,df.dijet_phi)
  df["Diphoton_dijet_dR"] = np.sqrt( dphi(df.Diphoton_phi,df.dijet_phi)**2 + (df.Diphoton_eta-df.dijet_eta)**2 )
#   df.loc[df.category==8, "Diphoton_dijet_deta"] = common.dummy_val
#   df.loc[df.category==8, "Diphoton_dijet_dphi"] = common.dummy_val
#   df.loc[df.category==8, "Diphoton_dijet_dR"] = common.dummy_val

  #zgamma variables
  df["LeadPhoton_dijet_dR"] = np.sqrt( dphi(df.LeadPhoton_phi,df.dijet_phi)**2 + (df.LeadPhoton_eta-df.dijet_eta)**2 )
  df["SubleadPhoton_dijet_dR"] = np.sqrt( dphi(df.SubleadPhoton_phi,df.dijet_phi)**2 + (df.SubleadPhoton_eta-df.dijet_eta)**2 )
  df["LeadPhoton_dijet_lead_dR"] = np.sqrt( dphi(df.LeadPhoton_phi,df.dijet_lead_phi)**2 + (df.LeadPhoton_eta-df.dijet_lead_eta)**2 )
  df["SubleadPhoton_dijet_lead_dR"] = np.sqrt( dphi(df.SubleadPhoton_phi,df.dijet_lead_phi)**2 + (df.SubleadPhoton_eta-df.dijet_lead_eta)**2 )
  df["LeadPhoton_dijet_sublead_dR"] = np.sqrt( dphi(df.LeadPhoton_phi,df.dijet_sublead_phi)**2 + (df.LeadPhoton_eta-df.dijet_sublead_eta)**2 )
  df["SubleadPhoton_dijet_sublead_dR"] = np.sqrt( dphi(df.SubleadPhoton_phi,df.dijet_sublead_phi)**2 + (df.SubleadPhoton_eta-df.dijet_sublead_eta)**2 )
#   df.loc[df.category==8, "LeadPhoton_dijet_dR"] = common.dummy_val
#   df.loc[df.category==8, "SubleadPhoton_dijet_dR"] = common.dummy_val
#   df.loc[df.category==8, "LeadPhoton_dijet_sublead_dR"] = common.dummy_val
#   df.loc[df.category==8, "SubleadPhoton_dijet_sublead_dR"] = common.dummy_val

def add_MET_variables(df):
  # met_dphi variables already exist for diphoton and dijet_lead
  df["dijet_met_dPhi"] = dphi(df.MET_phi, df.dijet_phi)
#   df.loc[df.category==8, "dijet_met_dPhi"] = common.dummy_val

  df["dijet_sublead_met_dPhi"] = dphi(df.MET_phi, df.dijet_sublead_phi)
#   df.loc[df.category==8, "dijet_sublead_met_dPhi"] = common.dummy_val

def applyPixelVeto(df):
  pixel_veto = (df.LeadPhoton_pixelSeed==0) & (df.SubleadPhoton_pixelSeed==0)
  #df.drop(df[~pixel_veto].index, inplace=True)
  return df[pixel_veto]

def apply90WPID(df):
#   selection = (df.Diphoton_max_mvaID > -0.26) & (df.Diphoton_min_mvaID > -0.26) #FIXME ggbb DF have no max/min mvaID!
  selection = (df.LeadPhoton_mvaID > -0.26) & (df.SubleadPhoton_mvaID > -0.26)
  #df.drop(df[~selection].index, inplace=True)
  return df[selection]

def reduceMemory(df):
  print(df.info())
  for column in df.columns:
    if df[column].dtype == "float64":
      print("%s float64 -> float32"%column.ljust(50))
      df.loc[:, column] = df[column].astype("float32")
    elif df[column].dtype == "int64":
      print("%s  int64 -> uint8"%column.ljust(50))
      df.loc[:, column] = df[column].astype("uint8")
    else:
      print("%s %s -> %s"%(column.ljust(50), df[column].dtype, df[column].dtype))
  print(df.info())

def fixDtypes(df):
#   df.loc[:, "lead_lepton_id"] = df["lead_lepton_id"].astype("int8")
#   df.loc[:, "sublead_lepton_id"] = df["sublead_lepton_id"].astype("int8")
#   df.loc[:, "lead_lepton_charge"] = df["lead_lepton_charge"].astype("int8")
#   df.loc[:, "sublead_lepton_charge"] = df["sublead_lepton_charge"].astype("int8")
  
  df.loc[:, "process_id"] = df["process_id"].astype("uint16") #new IDs are large!
  df.loc[:, "year"] = df["year"].astype("uint16")

  df.loc[:, "LeadPhoton_pixelSeed"] = df["LeadPhoton_pixelSeed"].astype("uint8")
  df.loc[:, "SubleadPhoton_pixelSeed"] = df["SubleadPhoton_pixelSeed"].astype("uint8")

def checkNans(df):
  for column in df.columns:
    try:
      if np.isnan(df[column]).any():
        print(df.loc[np.isnan(df[column]), column])
        df.loc[:, column].replace(np.nan, common.dummy_val, inplace=True)
    except:
      pass

def checkInfs(df):
  for column in df.columns:
    try:
      if np.isinf(df[column]).any():
        print(df.loc[np.isinf(df[column]), column])
        df.drop(df.loc[np.isinf(df[column])].index, inplace=True)    
    except:
      pass  

def merge2016(df):
  df.loc[df.year==b"2016UL_pre", "year"] = "2016"
  df.loc[df.year==b"2016UL_pos", "year"] = "2016"

def add_dijet_phi(df):
  bjet1_px = df.dijet_lead_pt * np.cos(df.dijet_lead_phi)
  bjet1_py = df.dijet_lead_pt * np.sin(df.dijet_lead_phi)
  bjet2_px = df.dijet_sublead_pt * np.cos(df.dijet_sublead_phi)
  bjet2_py = df.dijet_sublead_pt * np.sin(df.dijet_sublead_phi)

  dijet_px = bjet1_px + bjet2_px
  dijet_py = bjet1_py + bjet2_py
  df["dijet_phi"] = np.arctan2(dijet_py, dijet_px)
#   df.loc[df.category==8, "dijet_phi"] = common.dummy_val

def dividePhotonPT(df):
  df["LeadPhoton_pt_mgg"] = df["LeadPhoton_pt"] / df["Diphoton_mass"]
  df["SubleadPhoton_pt_mgg"] = df["SubleadPhoton_pt"] / df["Diphoton_mass"]

def prefiringWeights(df):
  df.loc[:, "weight_L1_prefiring_sf_central"] = 1.0
  df.loc[:, "weight_L1_prefiring_sf_up"] = 1.0
  df.loc[:, "weight_L1_prefiring_sf_down"] = 1.0

def rescale2018lowMassMC(df):
  df.loc[df["process_id"]!= 0, "weight_central"] = df['weight_central']*common.LumiFactor

def selectSigProcs(df, proc_dict, sig_procs):
  data_bkg_ids = [proc_dict[proc] for proc in common.bkg_procs["all"]+["Data"]]
  sig_proc_ids = [proc_dict[proc] for proc in sig_procs]
  return df[df.process_id.isin(data_bkg_ids+sig_proc_ids)]

def main(parquet_input, parquet_output, summary_input, do_test, keep_features, sig_procs=None):
  if not do_test:
    df = pd.read_parquet(parquet_input)
  else:
    from pyarrow.parquet import ParquetFile
    import pyarrow as pa
    pf = ParquetFile(parquet_input) 
    iter = pf.iter_batches(batch_size = 10)
    first_ten_rows = next(iter) 
    df = pa.Table.from_batches([first_ten_rows]).to_pandas() 

  original_columns = list(df.columns)

  with open(summary_input, "r") as f:
    proc_dict = json.load(f)["sample_id_map"]

  if sig_procs != None:
    df = selectSigProcs(df, proc_dict, sig_procs)
   
  print(0)
  reduceMemory(df)
  
  print(1)
  df = applyPixelVeto(df)
  df = apply90WPID(df)

  print(2)
  prefiringWeights(df)
  print(2.2)
  checkNans(df)
  print(2.3)
  checkInfs(df)
  print(3)
  common.add_MX_MY(df, proc_dict)

  print(4)
#   add_dijet_phi(df)
  if common.LOW_MASS_MODE :
    print ("rescaling MC")
    rescale2018lowMassMC(df)
  print(5)
#   add_MET_variables(df)
  print(6)
  add_Deltas(df)
  print(7)
  dividePhotonPT(df)
  print(8)
  mass_variables.add_reco_MX(df)  
#   mass_variables.add_reco_MX_met4(df)
  mass_variables.add_Mggb(df)
#   mass_variables.add_Mggb_met1(df)
  #add_helicity_angles(df)
  #divide_pt_by_mgg(df)
  print(9)
  merge2016(df)
  print(10)

  print("Additional columns:")
  print(set(df.columns).difference(original_columns))
  print(11)
  fixDtypes(df)

  if keep_features != None:
    print (" k1 ",keep_features)
    keep_features = common.train_features[keep_features]
    print (" k2 ",keep_features)
    keep_features += list(filter(lambda x: "reco_" in x, df.columns)) #reco mass vars
    keep_features += list(filter(lambda x: "weight" in x, df.columns)) #add weights
    print (" k3 ",keep_features)
    keep_features += ["Diphoton_mass", "MX", "MY", "event", "year", "process_id"] #add other neccessary columns
    keep_features = list(set(keep_features)) #remove overlap in columns
    print (" k4 ",keep_features)
    df = df[keep_features]

  print("Final columns:")
  print(df.columns)

  print(12)

  df.to_parquet(parquet_output)
  return df

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--parquet-input', '-i', type=str, required=True)
  parser.add_argument('--parquet-output', '-o', type=str, required=True)
  parser.add_argument('--summary-input', '-s', type=str, required=True)
  parser.add_argument('--test', action="store_true", default=False)
  parser.add_argument('--keep-features', '-f', type=str, default=None)
  parser.add_argument('--batch', action="store_true")
  parser.add_argument('--batch-slots', type=int, default=1)
  parser.add_argument('--sig-procs', '-p', type=str, nargs="+", default=None)

  args = parser.parse_args()

  if args.batch:
    common.submitToBatch([sys.argv[0]] + common.parserToList(args), extra_memory=args.batch_slots)
  else:
    main(args.parquet_input, args.parquet_output, args.summary_input, args.test, args.keep_features, args.sig_procs)