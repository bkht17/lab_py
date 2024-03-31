head = snake_list[-1]
    new = SnakeBlock(head.x + d_row, head.y + d_col)
    snake_list.append(new)
    snake_list.pop(0)