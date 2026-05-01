def pancake_sort_recursive_v3_3_all_state(perm, percent=0.75):

    n = len(perm)
    perm = tuple(perm)
    max_len_moves = 0

    permute_search = {}
    permute_complete = {}

    target = tuple(i for i in range(n))

    # ---------------------------------------------------------------------------------

    def idxs_and_positions(arr):

        # value < arr[0] : left
        left_value = arr[0] - 1 if arr[0] else None
        left_idx = arr.index(left_value) if left_value is not None else None

        # arr[0] < value : right
        right_value = arr[0] + 1 if arr[0] < n - 1 else None
        right_idx = arr.index(right_value) if right_value else n

        return left_value, left_idx, right_value, right_idx


    def mask_step_including(perm):

        perm_ = list(perm)
        n = len(perm_)
        steps = [] if perm_[n-1] == n-1 else [n]

        _, left_idx, _, right_idx = idxs_and_positions(perm)

        while len(perm_) - 2:
            m = perm_.pop()
            if not (perm_[-1] - 1 == m or perm_[-1] + 1 == m):
                steps.append(len(perm_))

            if left_idx and left_idx not in steps:
                steps.append(left_idx)

            if right_idx and right_idx not in steps:
                steps.append(right_idx)

        return steps


    def check_and_write(arr, moves, idx):

        if not moves or (moves and moves[-1] != idx):
            arr_ = arr[idx - 1::-1] + arr[idx:]
            if arr_ == target:
                permute_complete[moves + (idx,)] = len(moves) + 1
            else:
                move_recursive(arr_, moves + (idx,))


    def move_recursive(arr, moves):

        if permute_complete or permute_search.get(arr):
            return

        len_moves = len(moves)

        permute_search[arr] = moves, len_moves

        left_value, left_idx, right_value, right_idx = idxs_and_positions(arr)

        if left_idx and left_idx != 1 and arr[left_idx - 1] + 1 != left_value:
            check_and_write(arr, moves, left_idx)

        if not right_value or (right_idx != 1 and arr[right_idx - 1] - 1 != right_value):
            check_and_write(arr, moves, right_idx)

    # ---------------------------------------------------------------------------------

    move_recursive(perm, ())

    if not permute_search:
        permute_search[perm] = (), 0

    while not permute_complete:

        for perm, (steps, _) in list(permute_search.items()):
            if permute_complete:
                break
            for idx in mask_step_including(perm):
                check_and_write(perm, steps, idx)
            permute_search.pop(perm)

    # ================

    return list(permute_complete.keys()), permute_search, 0, 0
