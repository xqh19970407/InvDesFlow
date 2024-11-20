import os
import argparse



parser = argparse.ArgumentParser(description="Generate crystals with specified parameters")
parser.add_argument("--device", type=int, default=0, help="CUDA device ID")
parser.add_argument("--count", type=int, default=200, help="Number of crystals to generate")
parser.add_argument("--batch_size", type=int, default=1000, help="Batch size for generation")
parser.add_argument("--model_path", type=str, default="your_ckpt_dir", help="Path to the model")
parser.add_argument("--dataset", type=str, default="your_dataset_name", help="Dataset name")
args = parser.parse_args()

device = args.device
device_name = device
os.environ["CUDA_VISIBLE_DEVICES"] = f"{device}"


for i in range(0, args.count):
    try:
        cmd = f'python scripts/generation.py --pt_name device_3090_{device_name}_{i} --batch_size {args.batch_size} --model_path {args.model_path} --dataset {args.dataset}'
        os.system(cmd)
    except Exception as e:
        print(e)