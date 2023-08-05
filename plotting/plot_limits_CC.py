import scipy.interpolate as spi
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep
mplhep.set_style("CMS")


def plotLimits2D(x,y, limits, ylabel, savename):
  
  plt.rcParams["figure.figsize"] = (12.5,10)

  mx = np.sort(np.unique(x))
  my = np.sort(np.unique(y))
  mx_edges = np.array([mx[0] - (mx[1]-mx[0])/2] + list(mx[:-1] + (mx[1:] - mx[:-1])/2) + [mx[-1] + (mx[-1]-mx[-2])/2])
  my_edges = np.array([my[0] - (my[1]-my[0])/2] + list(my[:-1] + (my[1:] - my[:-1])/2) + [my[-1] + (my[-1]-my[-2])/2])

  mx_edge_centers = (mx_edges[:-1]+mx_edges[1:])/2
  my_edge_centers = (my_edges[:-1]+my_edges[1:])/2
  interp_masses = []
  interp_limits = []
  for mxi in mx_edge_centers:
    for myi in my_edge_centers:
      interp_masses.append([mxi, myi])
  interp_masses = np.array(interp_masses)
  interp_limits = spi.griddata((x,y), limits, interp_masses, method="linear")
  plt.hist2d(interp_masses[:,0], interp_masses[:,1], [mx_edges, my_edges], weights=interp_limits,norm=matplotlib.colors.Normalize(vmin=0.1))
  
  cbar = plt.colorbar()
  cbar.set_label(ylabel)
  plt.xlabel(r"$m_X$ [GeV]")
  plt.ylabel(r"$m_Y$ [GeV]")

  mplhep.cms.label(llabel="Work in Progress", data=True, lumi=132, loc=0)

  plt.savefig(savename+".png")
  plt.savefig(savename+".pdf")
  
  plt.clf()

def json2limits(limits_json):
   x=[]
   y=[]
   limit=[]
   for d in limits_json:
    x.append(float(d["sig_proc"].split("_")[7]))
    y.append(float(d["sig_proc"].split("_")[9]))
    limit.append(float(d["optimal_limit"]))
   return np.array(x),np.array(y),np.array(limit)

if __name__=="__main__":
  
    with open("/home/users/azecchin/Analysis/ResonantGGTT/Outputs/XtoYH_ggbb_2018_HLT_MCfix_looper/CatOptim/optim_results.json") as f:
        limits_json = json.load(f) 
    with open("/home/users/azecchin/Analysis/ResonantGGTT/Outputs/XtoYH_ggbb_2018_noMX/CatOptim/optim_results.json") as f:
        noMX_limits_json = json.load(f) 
    with open("/home/users/azecchin/Analysis/ResonantGGTT/Outputs/XtoYH_DDGJets/CatOptim/optim_results.json") as f:
        noMX_DDGJ_limits_json = json.load(f) 
    with open("/home/users/azecchin/Analysis/ResonantGGTT/Outputs/XtoYH_DDGJets_noHLTbit_newMX_model/CatOptim/optim_results.json") as f:
        newMX_DDGJ_limits_json = json.load(f) 

    x,y,z = json2limits(newMX_DDGJ_limits_json)
    ylabel=r"$\sigma(pp\rightarrow X)Br(X \rightarrow YH \rightarrow\gamma\gamma b b)$[fb]"
    plotLimits2D(x,y,z,ylabel,"limits")
