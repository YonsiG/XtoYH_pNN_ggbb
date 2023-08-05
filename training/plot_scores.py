import numpy as np
from plotting.training_plots import plotOutputScore

parser = argparse.ArgumentParser()

parser.add_argument('--parquet-input', '-i', type=str, required=True)
parser.add_argument('--summary-input', '-s', type=str, required=True)
parser.add_argument('--outdir', '-o', type=str, required=True)

args = parser.parse_args()


output_bkg_MC= "test" 
proc_dict= "test" 
sig_proc= "test"
args.outdir= "test" 
sig_proc= "test"
print(">> Plotting output scores")
for sig_proc in args.eval_sig_procs:
  print(sig_proc)
  output_sig = output_df[output_df.process_id == proc_dict[sig_proc]]
  with np.errstate(divide='ignore', invalid='ignore'): plotOutputScore(output_data, output_sig, output_bkg_MC, proc_dict, sig_proc, os.path.join(args.outdir, sig_proc))
