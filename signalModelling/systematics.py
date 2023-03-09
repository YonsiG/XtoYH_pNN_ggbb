import pandas as pd
import numpy as np

import scipy.interpolate as spi

import argparse
import os
import json
import common
import sys

import tracemalloc

from numba import jit

@jit(nopython=True)
def go_fast(hist, bin_edges, l, h):
  min_width = h-l
  for i in range(len(hist)):
    sumw = 0
    for j in range(i, len(hist)):
      sumw += hist[j]
      if sumw >= 0.6827:
        width = bin_edges[j+1]-bin_edges[i]

        #correct for over counting, i.e. estimate where in this bin we hit 0.6827
        width -= (bin_edges[1]-bin_edges[0]) * (sumw-0.6827) / hist[j]

        if width < min_width:
          min_width = width
          #print(bin_edges[i], bin_edges[j], (bin_edges[j]+bin_edges[i])/2)
        break
    if sumw < 0.6827: #no more 68% windows
      break
  return min_width

def debug(mgg, w, my, w_normed, s, l, h):
  #mgg = mgg.to_numpy()
  #w = w.to_numpy()
  #w_normed = w_normed.to_numpy()
  #s = s.to_numpy()

  print()
  print(w_normed)
  print(mgg)
  print(w_normed[s])
  print(mgg[s])
  print(sum(w_normed))
  print(sum(w_normed[s]))
  print(sum(w_normed[(mgg>=l)&(mgg<=h)]))
  print(np.average(mgg[s], weights=w[s]))
  print(np.std(mgg[s]))
  sort = np.argsort(mgg)
  mgg_sort = mgg[sort]
  w_sort = w_normed[sort]
  print(w_sort)
  print(mgg_sort)
  cs = np.cumsum(w_sort)
  q = lambda x: mgg_sort[np.argmin(abs(cs-x))]
  print(q(0.05), q(0.1), q(0.16), q(0.5), q(1-0.16), q(1-0.1), q(1-0.05))
  print(l, h)

def getEffSigma(mgg, w, my):
  assert len(w) >= 100
  assert sum(w) > 0

  mgg = mgg.to_numpy()
  w = w.to_numpy()

  mgg = mgg[w>0]
  w = w[w>0]

  if Y_gg:
    l = my - 10*(my/125.0)
    h = my + 10*(my/125.0)
  else:
    l = 125 - 10
    h = 125 + 10
  s = (mgg >= l) & (mgg <= h)
  
  # w_normed = w / sum(w)
  # assert np.isclose(sum(w_normed), 1)
  # #debug(mgg, w, my, w_normed, s, l, h)
  # if sum(w_normed[s]) < 0.6827:
  #   print("Warning: %.2f (< 68%%) of signal (my=%d) was found in range used for effSigma"%(sum(w_normed[s]), my))
  #   return h-l

  w_normed = w / sum(w[s]) # normalise according to events falling in window
  #w_normed = w / sum(w)

  hist, bin_edges = np.histogram(mgg[s], bins=300, range=(l,h), weights=w_normed[s])
  
  min_width = go_fast(hist, bin_edges, l, h)
  assert min_width != h-l
  assert min_width != 0
  
  return min_width / 2

# def getEffSigma(mgg, w, my):
#   return np.std(mgg)

def getMean(mgg, w, my):
  if Y_gg:
    l = my - 10*(my/125.0)
    h = my + 10*(my/125.0)
  else:
    l = 125 - 10
    h = 125 + 10
  s = (mgg >= l) & (mgg <= h)

  return np.average(mgg[s], weights=w[s])
  #return np.median(mgg[s])

# def getMean(mgg, w):
#   assert len(w) >= 100
#   assert sum(w) > 0
#   w_normed = w / sum(w)

#   #l = mgg.quantile(0.05)
#   #h = mgg.quantile(0.95)
#   l = 115
#   h = 135

#   hist, bin_edges = np.histogram(mgg, bins=2000, range=(l,h), weights=w_normed)

#   idx = np.argmax(hist)
#   mean = (bin_edges[idx] + bin_edges[idx+1])/2

#   return mean

def testEffSigma(scale=0.5, loc=125, size=10000):
  mgg = np.random.normal(loc=loc, scale=scale, size=size)
  w = np.ones_like(mgg)

  # import matplotlib
  # matplotlib.use("Agg")
  # import matplotlib.pyplot as plt
  # plt.hist(mgg, bins=100, range=(120,130), weights=w)
  # plt.savefig("eff_sigma_test.png")

  effSigma = getEffSigma(mgg, w, 125.0)
  print(effSigma)

def rename_btag_systematics(df):
  btag_columns = list(filter(lambda x: ("btag" in x) and ("central" not in x), df.columns))
  if len(btag_columns) == 0: return None
  
  mapper = {}
  for col in btag_columns:
    col_split = col.split("_")
    col_split[-1], col_split[-2] = col_split[-2], col_split[-1] #swap last two bits
    mapper[col] = "_".join(col_split)

  df.rename(mapper, axis=1, inplace=True)

  central_btag_col = list(filter(lambda x: ("btag" in x) and ("central" in x), df.columns))[0]

  btag_columns = filter(lambda x: ("btag" in x) and ("up" in x), df.columns)
  for col in btag_columns:
    df["%s_central"%"_".join(col.split("_")[:-1])] = df[central_btag_col]
  df.drop(central_btag_col, axis=1, inplace=True)

def deriveYieldSystematic(df, systematic, mass):
  #print(">> Doing yields")
  mx = int(mass.split("_")[0])
  my = int(mass.split("_")[1])

  central = df.loc[(df.MX==mx)&(df.MY==my), "weight_%s_central"%systematic].sum()
  up = df.loc[(df.MX==mx)&(df.MY==my), "weight_%s_up"%systematic].sum()
  down = df.loc[(df.MX==mx)&(df.MY==my), "weight_%s_down"%systematic].sum()

  if central == 0:
    variation_mean = 1.0
  else:
    variation_up = 1 + abs(1 - up/central)
    variation_down = 1 + abs(1 - down/central)
    variation_mean = (variation_up + variation_down)/2

    # print(variation_down, variation_down, abs(variation_up-variation_mean)/variation_mean, abs(variation_down-variation_mean)/variation_mean)
    # if (abs(variation_up-variation_mean)/variation_mean) > 0.1:
    #   print("Up variation too different from mean")
    #   print(variation_mean, variation_up,abs(variation_up-variation_mean)/variation_mean )
    # if (abs(variation_down-variation_mean)/variation_mean) > 0.1:
    #   print("down variation too different from mean")
    #   print(variation_mean, variation_down,abs(variation_down-variation_mean)/variation_mean )

  return float(variation_mean)

def getYieldSystematicsNames(original_df):
  rename_btag_systematics(original_df)
  yield_systematics = []
  for col in original_df.columns:
    if "central" in col and ("weight_central" not in col):
      yield_systematics.append("_".join(col.split("_")[1:-1]))

  return yield_systematics

def deriveParquetYieldSystematic(dfs, systematic, mass):
  #print(">> Doing parquet yields")
  mx = int(mass.split("_")[0])
  my = int(mass.split("_")[1])

  df_up = dfs["%s_up"%systematic]
  df_down = dfs["%s_down"%systematic]
  assert len(df_up) > 0
  assert len(df_down) > 0

  up = df_up.loc[(df_up.MX==mx)&(df_up.MY==my), "weight"].sum()
  down = df_down.loc[(df_down.MX==mx)&(df_down.MY==my), "weight"].sum()

  if up+down == 0:
    variation_mean = 1.0
  else:
    variation_mean = 1 + abs(up - down) / (up + down)

  return float(variation_mean)

def getParquetShapeVariations(f, df_up, df_down):
  assert len(df_up) > 0
  assert len(df_down) > 0

  up = f(df_up)
  down = f(df_down)
  assert (up + down) != 0, print(df_up, df_down)

  variation_mean = (up - down) / (up + down)
  return float(variation_mean)

def deriveParquetShapeSystematics(dfs, systematic, mass):
  #print(">> Doing parquet shape yields")
  mx = int(mass.split("_")[0])
  my = int(mass.split("_")[1])

  df_up = dfs["%s_up"%systematic]
  df_down = dfs["%s_down"%systematic]

  yields = lambda df: df.loc[(df.MX==mx)&(df.MY==my), "weight"].sum()                                                 if sum((df.MX==mx)&(df.MY==my)) >= 100 else 1.0
  sigmas = lambda df: getEffSigma(df[(df.MX==mx)&(df.MY==my)].Diphoton_mass, df[(df.MX==mx)&(df.MY==my)].weight, my)  if sum((df.MX==mx)&(df.MY==my)) >= 100 else 1.0
  means =  lambda df:     getMean(df[(df.MX==mx)&(df.MY==my)].Diphoton_mass, df[(df.MX==mx)&(df.MY==my)].weight, my)          if sum((df.MX==mx)&(df.MY==my)) >= 100 else 1.0

  consts = {}
  consts["const_rate_%s"%systematic] = getParquetShapeVariations(yields, df_up, df_down)
  consts["const_sigma_%s"%systematic] = getParquetShapeVariations(sigmas, df_up, df_down)
  consts["const_mean_%s"%systematic] = getParquetShapeVariations(means, df_up, df_down)

  return consts

def deriveSystematics(dfs, original_outdir):
  yield_systematics = getYieldSystematicsNames(dfs["nominal"])
  #parquet_yield_systematics = ["JER", "JES", "MET_JER", "MET_JES", "MET_Unclustered", "Muon_pt", "Tau_pt"]
  parquet_yield_systematics = ["JER", "JES", "MET_JES", "MET_Unclustered", "Muon_pt", "Tau_pt"]
  parquet_shape_systematics = ["fnuf", "material", "scale", "smear"]
  #parquet_yield_systematics = ["JER"]
  #parquet_shape_systematics = ["fnuf"]
  
  systematics = {}
  with open(os.path.join(original_outdir, "model.json"), "r") as f:
    sig_model = json.load(f)

  for year in sig_model.keys():
  #for year in ["2016"]:
    systematics[year] = {}
    for SR in sig_model[year].keys():
    #for SR in ["1", "2"]:
      print(year, SR)
      systematics[year][SR] = {}

      year_SR_dfs = {}
      for key in dfs.keys():
        df = dfs[key]
        year_SR_dfs[key] = df[(df.year==int(year))&(df.SR==int(SR))]

      for mass in sig_model[year][SR].keys():
        print(mass)
        #check if systematics already calculated
        closest_mass = sig_model[year][SR][mass]["this mass"]["closest_mass"]
        if closest_mass not in systematics[year][SR].keys():
          systematics[year][SR][closest_mass] = {}
          for systematic in yield_systematics:
            systematics[year][SR][closest_mass][systematic] = deriveYieldSystematic(year_SR_dfs["nominal"], systematic, closest_mass)
          for systematic in parquet_yield_systematics:
            systematics[year][SR][closest_mass][systematic] = deriveParquetYieldSystematic(year_SR_dfs, systematic, closest_mass)
          for systematic in parquet_shape_systematics:
            #print(systematic)
            systematics[year][SR][closest_mass].update(deriveParquetShapeSystematics(year_SR_dfs, systematic, closest_mass))

        systematics[year][SR][mass] = systematics[year][SR][closest_mass].copy()
        if closest_mass == mass:
          systematics[year][SR][mass]["interpolation"] = 1.0
        else:
          systematics[year][SR][mass]["interpolation"] = sig_model[year][SR][mass]["this mass"]["norm_systematic"]

  with open(os.path.join(original_outdir, "systematics.json"), "w") as f:
    json.dump(systematics, f, indent=4, sort_keys=True)

def addMigrationSystematics(outdir):
  with open(os.path.join(outdir, "model.json"), "r") as f:
    sig_model = json.load(f)
  with open(os.path.join(outdir, "systematics.json"), "r") as f:
    systematics = json.load(f)

  years = sorted(list(sig_model.keys()))
  SRs = sorted(list(sig_model[years[0]].keys()))
  masses = sorted(list(sig_model[years[0]][SRs[0]].keys()))

  print(years)
  print(SRs)

  for year in years:
    for SR in SRs[:-1]:
      masses = sig_model[year][SR].keys()
      SRp1 = str(int(SR)+1)
      sys_name = "Interpolation_migration_%s_%s"%(SR, SRp1)

      for m in masses:
        yield1 = sig_model[year][SR][m]["this mass"]["norm"]
        yield2 = sig_model[year][SRp1][m]["this mass"]["norm"]

        if (yield1 == 0) or (yield2 == 0):
          up1 = up2 = down1 = down2 = 1.0
        else:
          interpolation_uncert1 = systematics[year][SR][m]["interpolation"]
          interpolation_uncert2 = systematics[year][SRp1][m]["interpolation"]

          if interpolation_uncert1 >= 1.5 or interpolation_uncert2 >= 1.5:
            print(year, SR, m, interpolation_uncert1, interpolation_uncert2)

          up1 = 1 + ((interpolation_uncert2-1)*yield2) / yield1
          down1 = 1 - (interpolation_uncert1 - 1)
          assert down1 > 0

          up2 = 1 + ((interpolation_uncert1-1)*yield1) / yield2
          down2 = 1 - (interpolation_uncert2 - 1)
          assert down2 > 0

        for j in SRs:
          if j == SR:
            systematics[year][j][m][sys_name+"_left"] = up1
            systematics[year][j][m][sys_name+"_right"] = down1
          elif j == SRp1:
            systematics[year][j][m][sys_name+"_left"] = down2
            systematics[year][j][m][sys_name+"_right"] = up2
          else:
            systematics[year][j][m][sys_name+"_left"] = 1.0
            systematics[year][j][m][sys_name+"_right"] = 1.0

  with open(os.path.join(outdir, "systematics.json"), "w") as f:
    json.dump(systematics, f, indent=4, sort_keys=True)

def tagSignals(df, optim_dir, proc_dict):
  df["SR"] = -1

  with open(os.path.join(optim_dir, "optim_results.json"), "r") as f:
    optim_results = json.load(f)

  for proc in proc_dict.keys():
    if proc_dict[proc] in np.unique(df.process_id):
      score_name = "intermediate_transformed_score_%s"%proc

      for entry in optim_results:
        if score_name == entry["score"]:
          boundaries = entry["category_boundaries"][::-1]
          break

      for i in range(len(boundaries)-1):
        selection = (df[score_name] <= boundaries[i]) & (df[score_name] > boundaries[i+1]) & (df.process_id == proc_dict[proc])
        df.loc[selection, "SR"] = i

  return df[df.SR!=-1]

def loadDataFrame(path, proc_dict, optim_dir, columns=None, sample_fraction=1.0):
  df = pd.read_parquet(path, columns=columns)
  df = df[df.y==1]
  #df = df[df.process_id==proc_dict["NMSSM_XYH_Y_tautau_H_gg_MX_1000_MY_600"]]
  if sample_fraction != 1.0 :
    df = df.sample(frac=sample_fraction)  

  common.add_MX_MY(df, proc_dict)
  tagSignals(df, optim_dir, proc_dict)
  df = df[filter(lambda x: "score" not in x, df.columns)]
  return df

def getColumns(path):
  columns = common.getColumns(path)
  columns = list(filter(lambda x: x[:5] != "score", columns))
  columns = list(filter(lambda x: ("intermediate_transformed_score" in x), columns)) + ["Diphoton_mass", "process_id", "weight", "y", "year"]
  return columns

def loadDataFrames(args):
  with open(args.summary_input) as f:
    proc_dict = json.load(f)['sample_id_map']
  
  dfs = {}
  
  tracemalloc.start()
  for path in os.listdir(args.parquet_input):
    if (".parquet" in path) and ("nominal" not in path):
      print(path, np.array(tracemalloc.get_traced_memory())/(1024*1024*1024))
      full_path = os.path.join(args.parquet_input, path)

      df = loadDataFrame(full_path, proc_dict, args.optim_dir, columns=getColumns(full_path), sample_fraction=args.dataset_fraction)
      name = "_".join(path.split(".parquet")[0].split("_")[1:])
      dfs[name] = df
  tracemalloc.stop()

  #load nominal dataframe
  nominal_path = os.path.join(args.parquet_input, "merged_nominal.parquet")

  columns = getColumns(full_path) #columns from last systematic file
  columns.remove("weight")
  columns += list(filter(lambda x: "weight" in x, common.getColumns(nominal_path))) #add weight systematics

  df = loadDataFrame(nominal_path, proc_dict, args.optim_dir, columns=columns, sample_fraction=args.dataset_fraction) #get columns from last systematic file
  dfs["nominal"] = df
  
  #print(dfs)
  return dfs

def main(args):
  if args.batch:
    common.submitToBatch([sys.argv[0]] + common.parserToList(args), extra_memory=args.batch_slots)
    return True

  dfs = loadDataFrames(args)

  nominal_masses = np.sort(np.unique(dfs["nominal"].MX))
  #masses = np.arange(nominal_masses[0], nominal_masses[-1]+args.step, args.step, dtype=int)
  
  deriveSystematics(dfs, args.outdir)
  addMigrationSystematics(args.outdir)

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--parquet-input', '-i', type=str, required=True)
  parser.add_argument('--optim-dir', '-r', type=str, required=True)
  parser.add_argument('--summary-input', '-s', type=str, required=True)
  parser.add_argument('--outdir', '-o', type=str, required=True)
  parser.add_argument('--step', type=float, default=10.0)
  parser.add_argument('--batch', action="store_true")
  parser.add_argument('--batch-slots', type=int, default=2)
  parser.add_argument('--Y-gg', action="store_true")

  parser.add_argument('--dataset-fraction', type=float, default=1.0)
  args = parser.parse_args()

  os.makedirs(args.outdir, exist_ok=True)

  Y_gg = args.Y_gg #global variable to tell getMean and getEffSigma what ranges to look in

  main(args)