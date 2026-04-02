#Bài 1: Two Sum (Pythonic version) 
#Yêu cầu:
# Cho mảng số nguyên nums và số target, trả về 2 index sao cho tổng = target.
nums = [2, 7, 11, 15]



for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == 9:
            print([i, j])