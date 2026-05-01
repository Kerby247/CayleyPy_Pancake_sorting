def parse_permutation(raw: str) -> list[int]:
    """Parse a comma-separated permutation string into integer positions."""
    return [int(token) for token in raw.split(',') if token]


def pancake_sort_path(perm: Iterable[int]) -> list[str]:

    arr = list(perm)
    n = len(arr)
    moves: list[str] = []

    for target in range(n, 1, -1):
        desired_value = target - 1
        idx = arr.index(desired_value)

        if idx == target - 1:
            continue  # already in place

        if idx != 0:
            moves.append(f'R{idx + 1}')
            arr[: idx + 1] = reversed(arr[: idx + 1])

        moves.append(f'R{target}')
        arr[:target] = reversed(arr[:target])

    return moves


def pancake_sort_input(perm: Iterable[int]) -> list[int]:
    
    arr = list(perm)
    n = len(arr)
    moves: list[int] = []

    print(f'Len: {n}, Permutation: {arr}')
    move = int(input(f'Move:{len(moves) + 1:2d} | R:').strip())

    while move:
        moves.append(move)
        arr[: move] = reversed(arr[: move])
        print(arr)
        move = int(input(f'Move:{len(moves) + 1:2d} | R:'))

    return moves


def prob_step(perm):
    perm_ = perm.copy()
    n = len(perm_)
    k = perm_[-1] == n - 1
    # k -= sum(perm_[:2]) == 1

    while len(perm_) - 1:
        m = perm_.pop()
        k += perm_[-1] - 1 == m or perm_[-1] + 1 == m
    return n - k


def compare():
    n_list = [5, 12, 15, 16, 20, 25, 30, 35, 40, 45, 50, 75, 100]
    for n in n_list:
        pos = (best_df.n == n)
        score = best_df.score[pos].sum()
        n_sum = best_df.n[pos].sum()
        prob_step = best_df.prob_step[pos].sum()

        print(f'n: {n} | sum n: {n_sum} | score: {score} | prob step: {prob_step} | potential: {score - prob_step}')
    print()
    print(f'sum n: {best_df.n.sum()} | score: {best_df.score.sum()} | prob step: {best_df.prob_step.sum()}')


def best_solution(submission_df, best_df=None, safe=False):

    if best_df is None:
        best_df = pd.read_csv(BEST_SUBMISSION_PATH)

    best_df = best_df.set_index('id')
    submission_df = submission_df.set_index('id')

    common_idx = best_df.index.intersection(submission_df.index)

    same_score_idx = []
    best_score_idx = []

    for idx in common_idx:
        if best_df.loc[idx, 'score'] == submission_df.loc[idx, 'score']:
            same_score_idx.append(idx)

        if best_df.loc[idx, 'score'] > submission_df.loc[idx, 'score']:
            best_score_idx.append(idx)
            best_df.loc[idx, ['solution', 'score']] = submission_df.loc[idx, ['solution', 'score']]

    if safe and best_score_idx:
        best_df.to_csv(BEST_SUBMISSION_PATH, index=False)
        print('Best submission updated.')

    return best_df.reset_index().sort_values('id'), {'best': len(best_score_idx),
                                                     'same': len(same_score_idx),
                                                     'worse': len(common_idx) - len(best_score_idx) - len(same_score_idx)}


def process_row(row, func=None, treshold=3, save=False, from_target=False):

    perm = parse_permutation(row['permutation'])

    if from_target:
        perm, _= revers_perm(perm)

    moves, _, mlen, i = func(perm, treshold)

    if from_target:
        steps = moves[0][::-1]
    else:
        steps = moves[0]

    path_str = '.'.join(f'R{k}' for k in steps) if moves else 'UNSOLVED'

    if save:
        id_ = row['id']
        n = int(row['n'])
        print(f'id: {id_} - complete')

        with open(TEMP_ROOT / f'n_{n}.txt', mode='a') as file_:
            file_.write(f'{id_} - ' + path_str + '\n')

    return {
        'id': row['id'],
        'permutation': row['permutation'],
        'solution': path_str,
        'score': len(steps),
        'n': int(row['n']),
        'mlen': mlen,
        'iter': i
    }


def revers_perm(perm):
    code_dict = {}
    decode_dict = {}
    for i, n in enumerate(perm):
        code_dict[n] = i
        decode_dict[i] = n
    reversed_perm = [code_dict[i] for i in range(len(perm))]
    return reversed_perm, decode_dict


def check_steps(df):
    for row in df.to_dict('records'):
        perm = parse_permutation(row['permutation'])
        steps = list(map(int, row['solution'].lstrip('R').split('.R')))
        for idx in steps:
            perm[:idx] = perm[:idx][::-1]
        if perm != list(range(len(perm))):
            id_perm = row['id']
            print(f'Wrong solution for id{id_perm}')

check_steps(best_df)


def print_search(perm_dict):
    if perm_dict:
        for key, item in perm_dict.items():
            print(f'{key} | {item}')
    else:
        print(None)
