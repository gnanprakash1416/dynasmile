import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import random
def generate_random_sequence(length, num_zeros):
    # Ensure the range of generated numbers is large enough to prevent duplicates
    if length - num_zeros < 10:
        raise ValueError("A larger number range is needed to prevent duplicates.")
    
    # Generate unique random numbers
    unique_numbers = random.sample(range(1, length - num_zeros + 1), length - num_zeros)
    
    # Add the required number of zeros
    random_zeros = [0] * num_zeros
    complete_sequence = unique_numbers + random_zeros
    
    # Shuffle the sequence
    random.shuffle(complete_sequence)
    
    return complete_sequence
# Example: Generate a random sequence of length 100 with 10 zeros
def lognormal_map_values(data_ori, mu=None, sigma=None):
    data=np.array(data_ori)
    non_zero_indices = np.nonzero(data)[0]
    non_zero_values = data[non_zero_indices]
    # 2. 找到非零值的最大值和最小值
    min_value = np.min(non_zero_values)
    max_value = np.max(non_zero_values)
    # 3. 创建一个新的数组来保存最终结果
    new_data = data.copy()
    # 4. 将最大值和最小值替换为100和1
    new_data[non_zero_indices[non_zero_values == min_value]] = 1
    new_data[non_zero_indices[non_zero_values == max_value]] = 100
    # 5. 生成符合对数正态分布的随机数
    # 这里设定对数正态分布参数
    mu, sigma = 2, 1  # 参数可根据需要调整
    # 生成与非0值数量相同的随机数，减去2以保留最大值和最小值
    lognormal_samples = np.random.lognormal(mu, sigma, size=len(non_zero_values) - 2)
    # 将随机数转为1到100之间的整数
    lognormal_samples = np.clip(np.round(lognormal_samples), 2, 99).astype(int)
    # 6. 替换其他非0值
    sample_index = 0
    for index in non_zero_indices:
        if new_data[index] != 1 and new_data[index] != 100:  # 只替换非最小值和最大值
            new_data[index] = lognormal_samples[sample_index]
            sample_index += 1
    print(new_data)
    return new_data
def moving_average(data, window_size=5):
    if window_size < 1:
        raise ValueError("window_size must be at least 1.")
    
    cumsum = np.cumsum(data)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    moving_avg = cumsum[window_size - 1:] / window_size
    moving_avg = np.concatenate((np.full(window_size - 1, np.nan), moving_avg))
    moving_avg = np.nan_to_num(moving_avg)  # Replace NaN with 0
    return moving_avg
def smooth_and_preserve_extrema(original_data, smoothed_data):
    optimized_data = smoothed_data.copy()
    if len(original_data) != len(smoothed_data):
        raise ValueError("The lengths of original and smoothed data do not match.")
    
    # Replace maximum value
    max_index = np.argmax(original_data)
    optimized_data[max_index] = np.round(np.max(original_data))
    
    # Replace minimum value
    min_index = np.argmin(original_data)
    optimized_data[min_index] = np.round(np.min(original_data))
    
    return optimized_data
def map_to_color(data, color_scale):
    norm_data = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))  
    norm_data = np.clip(norm_data, 0, 1)
    cmap = LinearSegmentedColormap.from_list('custom_cmap', color_scale)
    colors = cmap(norm_data)
    return (colors[:, :3]*255).astype(int)
def main():
    np.random.seed(0)
    sequence = generate_random_sequence(110, 10)
    data = sequence
    
    print("Original Data:", data)
    mapped_data = lognormal_map_values(data, mu=0, sigma=1)
    print("Mapped Data:", mapped_data)
    smoothed_data = moving_average(mapped_data, window_size=5)
    print("Smoothed Data:", smoothed_data)
    final_smoothed_data = smooth_and_preserve_extrema(mapped_data, smoothed_data)
    print("Final Smoothed Data (Preserving Extremes):", final_smoothed_data)
    
    color_scale = [(1, 1, 1),  # White
                   (102/255, 204/255, 102/255)]  # RGB(102, 204, 102)
    
    colors = map_to_color(final_smoothed_data, color_scale)
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(final_smoothed_data)), final_smoothed_data, c=colors/255.0, s=100)
    print(colors)
    plt.title('Smoothed Data with Color Mapping (White to Green)')
    plt.xlabel('Data Index')
    plt.ylabel('Data Value')
    plt.grid()
    plt.show()
    
if __name__ == "__main__":
    main()
    # 假设您的原始data序列如下
    data = np.array([0, 2, 0, 5, 3, 0, 1, 4, 0, 0])
    # 1. 找出非0值的索引和对应的值
    non_zero_indices = np.nonzero(data)[0]
    non_zero_values = data[non_zero_indices]
    # 2. 找到非零值的最大值和最小值
    min_value = np.min(non_zero_values)
    max_value = np.max(non_zero_values)
    # 3. 创建一个新的数组来保存最终结果
    new_data = data.copy()
    # 4. 将最大值和最小值替换为100和1
    new_data[non_zero_indices[non_zero_values == min_value]] = 1
    new_data[non_zero_indices[non_zero_values == max_value]] = 100
    # 5. 生成符合对数正态分布的随机数
    # 这里设定对数正态分布参数
    mu, sigma = 0, 1  # 参数可根据需要调整
    # 生成与非0值数量相同的随机数，减去2以保留最大值和最小值
    lognormal_samples = np.random.lognormal(mu, sigma, size=len(non_zero_values) - 2)
    # 将随机数转为1到100之间的整数
    lognormal_samples = np.clip(np.round(lognormal_samples), 2, 100).astype(int)
    # 6. 替换其他非0值
    sample_index = 0
    for index in non_zero_indices:
        if new_data[index] != 1 and new_data[index] != 100:  # 只替换非最小值和最大值
            new_data[index] = lognormal_samples[sample_index]
            sample_index += 1
    print("原始数据序列:", data)
    print("新的数据序列:", new_data)