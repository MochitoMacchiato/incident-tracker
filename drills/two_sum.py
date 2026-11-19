# def two_sum(nums, target):
#     seen = {}
#     for i, n in enumerate(nums):
#         need = target - n
#         if need in seen:
#             return [seen[need], i]
#         seen[n] = i
#     return []

# print(two_sum([2, 7, 11, 15], 9))
# print(two_sum([3, 2, 4], 6))
# print(two_sum([3, 3], 6))
# print(two_sum([1, 2], 10))
# print(two_sum([3, 5, 6, 4], 7))

def first_repeat(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return n
        seen.add(n)
    return None

print(first_repeat([1,2,3,2,1]))