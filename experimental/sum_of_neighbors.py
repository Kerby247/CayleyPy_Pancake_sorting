def find_and_flip(x, first, b):
    prev = -1          # предыдущий элемент (для первого это граница)
    curr = first
    pos = 0
    while True:
        if curr == x:
            # Нашли нужный блин
            p = b[curr] - prev   # следующий за x (правый сосед)
            # Обновляем суммы трёх блинов
            b[first] += p
            b[curr] -= p
            if p != -1:          # если x не последний
                b[p] += first - curr
            new_first = curr
            return pos, new_first, b
        # Вычисляем следующий блин
        next_val = b[curr] - prev
        if next_val == -1:       # дошли до конца, не нашли (ошибка)
            return -1, first, b
        prev, curr = curr, next_val
        pos += 1
