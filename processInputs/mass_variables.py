"""
Number of mass variables I have experimented with. 
The variables use some combination of the visible particles and the MET.
"""

import numpy as np
import common

# def add_reco_MX_SVFit(df):
  # gg_px = df.Diphoton_pt * np.cos(0)
  # gg_py = df.Diphoton_pt * np.sin(0)
  # gg_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
  # gg_E = np.sqrt(df.Diphoton_mass**2 + gg_px**2 + gg_py**2 + gg_pz**2)

  # tt_px = df.pt_tautau_SVFit * np.cos(df.dPhi_ggtautau_SVFit)
  # tt_py = df.pt_tautau_SVFit * np.sin(df.dPhi_ggtautau_SVFit)
  # tt_eta = df.eta_tautau_SVFit_bdt * np.sign(df.Diphoton_eta)
  # tt_pz = df.pt_tautau_SVFit * np.sinh(tt_eta)
  # tt_E = np.sqrt(df.m_tautau_SVFit + tt_px**2 + tt_py**2 + tt_pz**2)

  # X_px = gg_px + tt_px
  # X_py = gg_py + tt_py
  # X_pz = gg_pz + tt_pz
  # X_E = gg_E + tt_E

  # df["reco_MX_SVFit"] = np.sqrt(X_E**2 - X_px**2 - X_py**2 - X_pz**2)
  # df["reco_MX_SVFit_mgg"] = df["reco_MX_SVFit"] / df.Diphoton_mass
  # df.loc[df.category == 8, "reco_MX_SVFit"] = common.dummy_val
  # df.loc[df.category == 8, "reco_MX_SVFit_mgg"] = common.dummy_val

def add_reco_MX(df):
  # I would move to ak 4vectors here 
  H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
  H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
  H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
  H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
  H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

  H2_px = df.dijet_pt * np.cos(df.dijet_phi)
  H2_py = df.dijet_pt * np.sin(df.dijet_phi)
  H2_pz = df.dijet_pt * np.sinh(df.dijet_eta)
  H2_P = df.dijet_pt * np.cosh(df.dijet_eta)
  H2_E = np.sqrt(H2_P**2 + df.dijet_mass**2)

#   H2_px = df.ditau_pt * np.cos(df.ditau_phi) 
#   H2_py = df.ditau_pt * np.sin(df.ditau_phi)
#   H2_pz = df.ditau_pt * np.sinh(df.ditau_eta)
#   H2_P = df.ditau_pt * np.cosh(df.ditau_eta)
#   H2_E = np.sqrt(H2_P**2 + df.ditau_mass**2)

  df["reco_MX"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)
  df["reco_MX_mgg"] = df["reco_MX"] / df["Diphoton_mass"]
  df["xcand_mass_mgg"] = df["xcand_mass"] / df["Diphoton_mass"]
#   df.loc[df.category == 8, "reco_MX"] = common.dummy_val
#   df.loc[df.category == 8, "reco_MX_mgg"] = common.dummy_val

def add_reco_MX_MET(df):
  H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
  H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
  H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
  H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
  H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

  H2_px = df.dijet_pt * np.cos(df.dijet_phi) + df.MET_pt * np.cos(df.MET_phi) 
  H2_py = df.dijet_pt * np.sin(df.dijet_phi) + df.MET_pt * np.sin(df.MET_phi)
  H2_pz = df.dijet_pt * np.sinh(df.dijet_eta) * 2
  H2_P = np.sqrt(H2_px**2 + H2_py**2 + H2_pz**2)
  H2_E = np.sqrt(H2_P**2 + df.dijet_mass**2)

#   H2_px = df.ditau_pt * np.cos(df.ditau_phi) + df.MET_pt * np.cos(df.MET_phi) 
#   H2_py = df.ditau_pt * np.sin(df.ditau_phi) + df.MET_pt * np.sin(df.MET_phi)
#   H2_pz = df.ditau_pt * np.sinh(df.ditau_eta) * 2
#   H2_P = np.sqrt(H2_px**2 + H2_py**2 + H2_pz**2)
#   H2_E = np.sqrt(H2_P**2 + df.ditau_mass**2)

  HH_px = H1_px + H2_px
  HH_py = H1_py + H2_py
  HH_pz = H1_pz + H2_pz
  HH_E = H1_E + H2_E

  df["reco_MX_MET"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)
  df["reco_MX_MET_mgg"] = df["reco_MX_MET"] / df["Diphoton_mass"]
#   df.loc[df.category == 8, "reco_MX_MET"] = common.dummy_val
#   df.loc[df.category == 8, "reco_MX_MET_mgg"] = common.dummy_val

def add_Mggb(df):
  H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
  H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
  H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
  H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
  H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

  
  H2_px = df.dijet_lead_pt * np.cos(df.dijet_lead_phi) 
  H2_py = df.dijet_lead_pt * np.sin(df.dijet_lead_phi)
  H2_pz = df.dijet_lead_pt * np.sinh(df.dijet_lead_eta)
  H2_P = df.dijet_lead_pt * np.cosh(df.dijet_lead_eta)
  H2_E = np.sqrt(H2_P**2 + df.dijet_lead_mass**2)

#   H2_px = df.lead_lepton_pt * np.cos(df.lead_lepton_phi)
#   H2_py = df.lead_lepton_pt * np.sin(df.lead_lepton_phi)
#   H2_pz = df.lead_lepton_pt * np.sinh(df.lead_lepton_eta)
#   H2_P = df.lead_lepton_pt * np.cosh(df.lead_lepton_eta)
#   H2_E = np.sqrt(H2_P**2 + df.lead_lepton_mass**2)

  HH_px = H1_px + H2_px
  HH_py = H1_py + H2_py
  HH_pz = H1_pz + H2_pz
  HH_E = H1_E + H2_E

  df["reco_Mggb"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)
  df["reco_Mggb_mgg"] = df["reco_Mggb"] / df["Diphoton_mass"]
  df["reco_Mggb_mgg2"] = df["reco_Mggb"] - df["Diphoton_mass"]


def add_Mggb_met1(df):
  H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
  H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
  H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
  H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
  H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

  H2_px = df.dijet_lead_pt * np.cos(df.dijet_lead_phi)
  H2_py = df.dijet_lead_pt * np.sin(df.dijet_lead_phi)
  H2_pz = df.dijet_lead_pt * np.sinh(df.dijet_lead_eta)
  H2_P = df.dijet_lead_pt * np.cosh(df.dijet_lead_eta)
  H2_E = np.sqrt(H2_P**2 + df.dijet_lead_mass**2)

  MET_px = df.MET_pt * np.cos(df.MET_phi)
  MET_py = df.MET_pt * np.sin(df.MET_phi)
  MET_pz = 0
  MET_E = np.sqrt(MET_px**2 + MET_py**2)

  HH_px = H1_px + H2_px + MET_px
  HH_py = H1_py + H2_py + MET_py
  HH_pz = H1_pz + H2_pz + MET_pz
  HH_E = H1_E + H2_E + MET_E

  df["reco_MggbMET"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)
  df["reco_MggbMET_mgg"] = df["reco_MggbMET"] / df["Diphoton_mass"]

# def add_Mggt_met2(df):
#   H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
#   H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
#   H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
#   H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
#   H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

#   H2_px = df.lead_lepton_pt * np.cos(df.lead_lepton_phi) + df.MET_pt * np.cos(df.MET_phi)
#   H2_py = df.lead_lepton_pt * np.sin(df.lead_lepton_phi) + df.MET_pt * np.sin(df.MET_phi)
#   H2_pz = df.lead_lepton_pt * np.sinh(df.lead_lepton_eta)
#   H2_P = H2_px**2 + H2_py**2 + H2_pz**2
#   H2_E = np.sqrt(H2_P**2 + 125**2)

#   HH_px = H1_px + H2_px
#   HH_py = H1_py + H2_py
#   HH_pz = H1_pz + H2_pz
#   HH_E = H1_E + H2_E

#   df["reco_Mggtau_met2"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)

# def add_Mggt_met3(df):
#   H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
#   H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
#   H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
#   H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
#   H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

#   H2_px = df.lead_lepton_pt * np.cos(df.lead_lepton_phi)
#   H2_py = df.lead_lepton_pt * np.sin(df.lead_lepton_phi)
#   H2_pz = df.lead_lepton_pt * np.sinh(df.lead_lepton_eta)
#   H2_P = df.lead_lepton_pt * np.cosh(df.lead_lepton_eta)
#   H2_E = np.sqrt(H2_P**2 + df.lead_lepton_mass**2)

#   MET_px = df.MET_pt * np.cos(df.MET_phi)
#   MET_py = df.MET_pt * np.sin(df.MET_phi)
#   MET_pz = H2_pz
#   MET_E = np.sqrt(MET_px**2 + MET_py**2 + MET_pz**2)

#   HH_px = H1_px + H2_px + MET_px
#   HH_py = H1_py + H2_py + MET_py
#   HH_pz = H1_pz + H2_pz + MET_pz
#   HH_E = H1_E + H2_E + MET_E

#   df["reco_Mggtau_met3"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)

# def add_Mggt_met4(df):
#   H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
#   H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
#   H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
#   H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
#   H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

#   H2_px = df.lead_lepton_pt * np.cos(df.lead_lepton_phi) + df.MET_pt * np.cos(df.MET_phi)
#   H2_py = df.lead_lepton_pt * np.sin(df.lead_lepton_phi) + df.MET_pt * np.sin(df.MET_phi)
#   H2_pz = df.lead_lepton_pt * np.sinh(df.lead_lepton_eta) * 2
#   H2_P = H2_px**2 + H2_py**2 + H2_pz**2
#   H2_E = np.sqrt(H2_P**2 + 125**2)

#   HH_px = H1_px + H2_px
#   HH_py = H1_py + H2_py
#   HH_pz = H1_pz + H2_pz
#   HH_E = H1_E + H2_E

#   df["reco_Mggtau_met4"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)

# def get_MET_pz(mh, ptx, pty, ptz, pmx, pmy):
#   a = mh**2*ptz
#   b = 2*pmx*ptx*ptz
#   c = 2*pmy*pty*ptz

#   d = mh**4
#   e = 4*(pmy*ptx-pmx*pty)**2
#   f = 4*mh**2*(pmx*ptx+pmy*pty)
#   g = (ptx**2+pty**2+ptz**2)

#   h = 2*(ptx**2+pty**2)

#   return (a + b + c + np.sqrt((d-e+f)*g))/h

# def add_Mggt_met3(df):
#   H1_px = df.Diphoton_pt * np.cos(df.Diphoton_phi)
#   H1_py = df.Diphoton_pt * np.sin(df.Diphoton_phi)
#   H1_pz = df.Diphoton_pt * np.sinh(df.Diphoton_eta)
#   H1_P = df.Diphoton_pt * np.cosh(df.Diphoton_eta)
#   H1_E = np.sqrt(H1_P**2 + df.Diphoton_mass**2)

#   H2_px = df.lead_lepton_pt * np.cos(df.lead_lepton_phi)
#   H2_py = df.lead_lepton_pt * np.sin(df.lead_lepton_phi)
#   H2_pz = df.lead_lepton_pt * np.sinh(df.lead_lepton_eta)
#   H2_P = df.lead_lepton_pt * np.cosh(df.lead_lepton_eta)
#   H2_E = np.sqrt(H2_P**2 + df.lead_lepton_mass**2)

#   MET_px = df.MET_pt * np.cos(df.MET_phi)
#   MET_py = df.MET_pt * np.sin(df.MET_phi)

#   MET_pz = get_MET_pz(125, H2_px, H2_py, H2_pz, MET_px, MET_py)
#   MET_E = np.sqrt(MET_px**2 + MET_py**2 + MET_pz**2)

#   HH_px = H1_px + H2_px + MET_px
#   HH_py = H1_py + H2_py + MET_py
#   HH_pz = H1_pz + H2_pz + MET_pz
#   HH_E = H1_E + H2_E + MET_E

#   df["reco_Mggtau_met3"] = np.sqrt(HH_E**2 - HH_px**2 - HH_py**2 - HH_pz**2)
