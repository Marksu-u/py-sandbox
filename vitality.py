import turtle
import re

PATH_1 = "m9.051 30.567 4.912-8.747L6.317 0c-4.42 1.194-8.74 10.209-4.721 17.789 1.931 3.64 7.455 12.778 7.455 12.778ZM5.73 28.263 3.593 26.85l-1.318-3.508h-.953L1.8 27.96l5.814 3.458zm30.17-1.412-2.135 1.412-1.884 3.154 5.812-3.458.478-4.616h-.955zm-22.947 9.557L19.745 48l6.72-11.575-6.72 1.06zm10.861-14.304-4.067-6.312-4.067 6.312 4.067 6.23z"
PATH_2 = "m29.29 31.904-4.564-8.074-4.979 7.482-4.979-7.482-4.563 8.074-3.37 2.176-.478 7.336h.956l1.315-6.228 1.803-.743 9.316 1.283 9.316-1.283 1.803.743 1.316 6.228h.955l-.478-7.336Zm8.606-14.115c4.022-7.58-.298-16.595-4.718-17.789l-7.642 21.82 4.905 8.747s5.526-9.139 7.455-12.778z"

def tokenize_path(d):
    token_pattern = re.compile(r'([a-zA-Z])|([-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)')
    tokens = []
    for match in token_pattern.finditer(d):
        cmd, num = match.groups()
        if cmd:
            tokens.append(cmd)
        elif num:
            tokens.append(float(num))
    return tokens

def draw_svg_path(pen, d, scale=12, offset_x=-20.0, offset_y=-24.0):
    tokens = tokenize_path(d)
    
    def to_turtle(x, y):
        tx = (x + offset_x) * scale
        ty = -(y + offset_y) * scale
        return tx, ty
        
    curr_x, curr_y = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    prev_ctrl_x, prev_ctrl_y = 0.0, 0.0
    prev_cmd = ''
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, str):
            cmd = token
            i += 1
        else:
            if cmd == 'm': cmd = 'l'
            elif cmd == 'M': cmd = 'L'
            
        if cmd == 'm':
            dx, dy = tokens[i], tokens[i+1]
            i += 2
            curr_x += dx
            curr_y += dy
            pen.penup()
            pen.goto(to_turtle(curr_x, curr_y))
            pen.pendown()
            pen.begin_fill()
            start_x, start_y = curr_x, curr_y
        elif cmd == 'M':
            x, y = tokens[i], tokens[i+1]
            i += 2
            curr_x = x
            curr_y = y
            pen.penup()
            pen.goto(to_turtle(curr_x, curr_y))
            pen.pendown()
            pen.begin_fill()
            start_x, start_y = curr_x, curr_y
        elif cmd == 'l':
            dx, dy = tokens[i], tokens[i+1]
            i += 2
            curr_x += dx
            curr_y += dy
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'L':
            x, y = tokens[i], tokens[i+1]
            i += 2
            curr_x = x
            curr_y = y
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'h':
            dx = tokens[i]
            i += 1
            curr_x += dx
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'H':
            x = tokens[i]
            i += 1
            curr_x = x
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'v':
            dy = tokens[i]
            i += 1
            curr_y += dy
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'V':
            y = tokens[i]
            i += 1
            curr_y = y
            pen.goto(to_turtle(curr_x, curr_y))
        elif cmd == 'c':
            dx1, dy1 = tokens[i], tokens[i+1]
            dx2, dy2 = tokens[i+2], tokens[i+3]
            dx, dy = tokens[i+4], tokens[i+5]
            i += 6
            
            p0 = (curr_x, curr_y)
            p1 = (curr_x + dx1, curr_y + dy1)
            p2 = (curr_x + dx2, curr_y + dy2)
            p3 = (curr_x + dx, curr_y + dy)
            
            steps = 25
            for s in range(1, steps + 1):
                t_val = s / steps
                bx = (1-t_val)**3*p0[0] + 3*(1-t_val)**2*t_val*p1[0] + 3*(1-t_val)*t_val**2*p2[0] + t_val**3*p3[0]
                by = (1-t_val)**3*p0[1] + 3*(1-t_val)**2*t_val*p1[1] + 3*(1-t_val)*t_val**2*p2[1] + t_val**3*p3[1]
                pen.goto(to_turtle(bx, by))
                
            curr_x, curr_y = p3
            prev_ctrl_x, prev_ctrl_y = p2
        elif cmd == 'C':
            x1, y1 = tokens[i], tokens[i+1]
            x2, y2 = tokens[i+2], tokens[i+3]
            x, y = tokens[i+4], tokens[i+5]
            i += 6
            
            p0 = (curr_x, curr_y)
            p1 = (x1, y1)
            p2 = (x2, y2)
            p3 = (x, y)
            
            steps = 25
            for s in range(1, steps + 1):
                t_val = s / steps
                bx = (1-t_val)**3*p0[0] + 3*(1-t_val)**2*t_val*p1[0] + 3*(1-t_val)*t_val**2*p2[0] + t_val**3*p3[0]
                by = (1-t_val)**3*p0[1] + 3*(1-t_val)**2*t_val*p1[1] + 3*(1-t_val)*t_val**2*p2[1] + t_val**3*p3[1]
                pen.goto(to_turtle(bx, by))
                
            curr_x, curr_y = p3
            prev_ctrl_x, prev_ctrl_y = p2
        elif cmd == 's':
            dx2, dy2 = tokens[i], tokens[i+1]
            dx, dy = tokens[i+2], tokens[i+3]
            i += 4
            
            p0 = (curr_x, curr_y)
            if prev_cmd in ['c', 'C', 's', 'S']:
                p1 = (curr_x + (curr_x - prev_ctrl_x), curr_y + (curr_y - prev_ctrl_y))
            else:
                p1 = p0
                
            p2 = (curr_x + dx2, curr_y + dy2)
            p3 = (curr_x + dx, curr_y + dy)
            
            steps = 25
            for s in range(1, steps + 1):
                t_val = s / steps
                bx = (1-t_val)**3*p0[0] + 3*(1-t_val)**2*t_val*p1[0] + 3*(1-t_val)*t_val**2*p2[0] + t_val**3*p3[0]
                by = (1-t_val)**3*p0[1] + 3*(1-t_val)**2*t_val*p1[1] + 3*(1-t_val)*t_val**2*p2[1] + t_val**3*p3[1]
                pen.goto(to_turtle(bx, by))
                
            curr_x, curr_y = p3
            prev_ctrl_x, prev_ctrl_y = p2
        elif cmd in ['z', 'Z']:
            pen.goto(to_turtle(start_x, start_y))
            pen.end_fill()
            curr_x, curr_y = start_x, start_y
            
        prev_cmd = cmd

def main():
    screen = turtle.Screen()
    screen.setup(700, 700)
    screen.bgcolor("#111111")
    screen.title("Team Vitality Logo")
    
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    
    pen.color("#FFE600")
    pen.pensize(1)
    
    print("Drawing the Team Vitality Logo...")
    draw_svg_path(pen, PATH_1, scale=12, offset_x=-20.0, offset_y=-24.0)
    draw_svg_path(pen, PATH_2, scale=12, offset_x=-20.0, offset_y=-24.0)
    
    print("Finished! Click the drawing window to close.")
    screen.exitonclick()

if __name__ == "__main__":
    main()
