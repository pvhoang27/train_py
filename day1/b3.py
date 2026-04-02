# 🔹 Bài 3: Top K Frequent Elements

# Yêu cầu:
# Cho mảng nums, trả về k phần tử xuất hiện nhiều nhất
from collections import Counter

def topKFrequent(nums, k):
    # Bước 1: Đếm số lần xuất hiện
    count = Counter(nums)
    print("Tần suất:", count)

    # Bước 2: Lấy k phần tử xuất hiện nhiều nhất
    most_common = count.most_common(k)
    print("Top K:", most_common)

    # Bước 3: Chỉ lấy phần tử (bỏ số lần)
    result = []
    for num, freq in most_common:
        result.append(num)

    return result


# Test
nums = [1,1,1,2,2,3]
k = 2
print(topKFrequent(nums, k))