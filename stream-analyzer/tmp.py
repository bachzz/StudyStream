## detect facial landmarks -> crop left eye region

im = cv2.imread(fname)
im = np.copy(im).astype(np.float32)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
im = (im / 255.0 - mean) / std
im = torch.from_numpy(im).permute(2,0,1).unsqueeze(0)

# t = time.time()
output = model(im)
# print(f"[HRNet] {fname} - Elapsed time = {time.time()-t}")
score_map = output.data.cpu()
preds = decode_preds(score_map, torch.tensor([[128.0,128.0]]), torch.tensor([1.28]), [64, 64])

idx=0
left_idx = [60,61,62,63,64,65,66,67]
left_coords = np.zeros((8,2))
for x,y in preds[0]:
    x, y = int(x), int(y)
    if idx in left_idx:
        left_coords[left_idx.index(idx)] = [x,y]
        # cv2.circle(frame, (x,y), 1, (0, 0, 255), 2)
    idx = idx+1
left_coords_min = left_coords.min(axis=0).astype(int)
left_coords_max = left_coords.max(axis=0).astype(int)
left_w, left_h = left_coords_max-left_coords_min

## compute EAR 
p1 = left_coords[0]; p2 = left_coords[1]; p3 = left_coords[3]; p4 = left_coords[4]; p5=left_coords[5]; p6=left_coords[7]
EAR_ratio = (np.linalg.norm(p2-p6) + np.linalg.norm(p3-p5))/(2*np.linalg.norm(p1-p4))
os.popen(f'echo {EAR_ratio} > {item}/EAR/{fname.split("/")[-1].split(".png")[0]}.txt')