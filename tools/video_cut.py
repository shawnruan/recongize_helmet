import cv2
import os

# 读取视频文件
video_path = '/Users/ruanxiaoyang/Desktop/video_cap/4号罐顶平台2#20250108.mp4'
output_folder = "/Users/ruanxiaoyang/Desktop/video_frames"
os.makedirs(output_folder, exist_ok=True)  # 确保输出目录存在

cap = cv2.VideoCapture(video_path)

frame_count = 0  # 帧编号
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 构造文件名（使用 frame_count 作为编号）
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
    cv2.imwrite(frame_filename, frame)  # 保存帧

    frame_count += 1  # 递增帧编号

cap.release()
cv2.destroyAllWindows()

print(f"Extracted {frame_count} frames to {output_folder}")