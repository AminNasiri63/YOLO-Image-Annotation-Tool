from .modules import *
from .Classes import *
from .constants import *

def ModifyLabels(path_data, folder_name):
    process_end = False
    new_folder = False

    def mouse_event(event, x, y, flags, param):
        nonlocal pts_l, pts_r, pts_m, pts_move

        x = max(0, min(x, w))
        y = max(0, min(y, h))

        if event == cv2.EVENT_LBUTTONDOWN:
            pts_l.append((x, y))

        elif event == cv2.EVENT_MOUSEMOVE:
            pts_move = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            pts_l.append((x, y))

        elif event == cv2.EVENT_RBUTTONDOWN:
            pts_r = (x, y)

        elif event == cv2.EVENT_MBUTTONDOWN:
            pts_m = (x, y)

    allData = ImagesLabels(path_data, folder_name)

    for txt, img, num in allData:
        pts_l, pts_r, pts_m, pts_move, PtsFinal = [], (), (), (), []

        frame = cv2.imread(img)
        h, w, _ = frame.shape

        win_name = f"img: {num}"
        cv2.namedWindow(win_name, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(win_name, w, h)
        # cv2.moveWindow(win_name, 300, 20)
        cv2.setMouseCallback(win_name, mouse_event)

        with open(txt, 'r') as f:
            while line := f.readline():
                bbx = Box.CreateFromtxt(line, w, h)
                PtsFinal.append(bbx)

        while True:
            clone = frame.copy()

            for ind, box in enumerate(PtsFinal):
                cl, x1, y1, x2, y2 = box.YoloToXYXY()

                if pts_move and box.PointInRect(pts_move) and not pts_l:
                    cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0), -1)
                    cv2.circle(clone, (x1, y1), 10, (255, 0, 0), -1)
                    cv2.circle(clone, (x2, y2), 10, (255, 0, 0), -1)
                    clone = cv2.addWeighted(clone, alpha, frame, 1 - alpha, 0)
                else:
                    cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.circle(clone, (x1, y1), 10, (255, 0, 0), 2)
                    cv2.circle(clone, (x2, y2), 10, (255, 0, 0), 2)

                if y1 > 50:
                    cv2.putText(clone, f"C:{int(cl)}", (x1, y1 - 10), 0, 0.6, (0, 255, 255), 2)
                else:
                    cv2.putText(clone, f"C:{int(cl)}", (x1, y2 + 20), 0, 0.6, (0, 255, 255), 2)

                if pts_r and box.PointInRect(pts_r):
                        PtsFinal.pop(ind)
                        pts_r = ()

                if pts_m and box.PointInRect(pts_m):
                        box.DefineClass()
                        pts_m = ()

            if len(pts_l) == 1:
                move_bbx = False
                if pts_move:
                    for box_ in PtsFinal:
                        pts_l[0], move_bbx = box_.PointPositionCheck(pts_l[0], pts_move)

                        if move_bbx:
                            break

                    if not move_bbx:
                        cv2.rectangle(clone, pts_l[0], pts_move, (255, 0, 0), 2)
                        cv2.circle(clone, pts_l[0], 10, (255, 0, 0), 2)

            elif len(pts_l) == 2:
                if not move_bbx:
                    box = Box.CreateFromScreen(pts_l, w, h)

                    if box:
                        PtsFinal.append(box)

                        # _, x1, y1, x2, y2 = box.YoloToXYXY()
                        # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        # cv2.circle(clone, (x1, y1), 10, (255, 0, 0), 2)
                        # cv2.circle(clone, (x2, y2), 10, (255, 0, 0), 2)

                else:
                    box_.CheckBox()

                pts_l = []

            cv2.imshow(win_name, clone)
            k = cv2.waitKey(33)

            if k == ord('q'):
                process_end = True
                break

            elif k == ord('f'):
                new_folder = True
                break

            elif k == ord('s'):
                allData.Save(PtsFinal)
                cv2.destroyAllWindows()
                break

            elif k == ord('n'):
                cv2.destroyAllWindows()
                break

        if process_end or new_folder:
            break

    cv2.destroyAllWindows()

    return process_end