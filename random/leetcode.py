def findErrorNums(nums):
    print("Original nums:", nums)
    nums.sort()
    print("Sorted nums:", nums)

    for n in nums:
        print("\nChecking n:", n)

        pos = nums.index(n)
        print("nums.index(n):", pos)

        # This is your original boundary logic
        if pos < len(nums) - 2:
            print("Comparing nums[pos] and nums[pos + 1]:", nums[pos], nums[pos + 1])

            if n == nums[pos + 1]:
                print("Duplicate found at pos:", pos)
                print("Returning:", [pos + 1, n + 1])
                return [pos + 1, n + 1]

    print("No duplicate found with your logic")
    return None


# -------- TESTS --------
print(findErrorNums([1, 2, 2, 4]))
# print(findErrorNums([1, 1]))
# print(findErrorNums([2, 2]))
# print(findErrorNums([1, 2, 3, 3]))