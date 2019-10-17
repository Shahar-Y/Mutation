import cv2
import new_constants as C

def create_db():
    cell_size = 0.03
    sight_val = int(255/(C.MAX_SIGHT - C.MIN_SIGHT + 1))
    speed_val = int(255/(C.MAX_VEL - C.MIN_VEL + 1))
    print('sight_val: ' + str(sight_val) + ' speed_val:' + str(speed_val))
    print(str(C.MAX_SIZE), ' ', str(C.MAX_SIGHT), ' ', str(C.MAX_VEL))
    for st in range(0, C.MAX_SIGHT+1):
        for spd in range(0, C.MAX_VEL+1):
            for sz in range(0, C.MAX_SIZE+1):
                # get the original image
                print('_'+str(st)+'_'+str(spd)+'_'+str(sz))
                image = cv2.imread("src/newUI/images/original_cell.png")
                overlay = image.copy()
                output = image.copy()


                # draw a circle
                color = (st*sight_val, spd*speed_val, 50)
                cv2.circle(overlay, (125, 125), 115, color, -1)

                # create the overlayed image
                alpha = 0.7
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
                icon_name = 'src/images/icons/Cell_'+str(st)+'_'+str(spd)+'_'+str(sz)+'.png'
                cv2.imwrite(icon_name, output)

                src = cv2.imread(icon_name, 1)
                tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                _,alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
                b, g, r = cv2.split(src)
                rgba = [b,g,r, alpha]
                dst = cv2.merge(rgba, 4)
                dst = cv2.resize(dst, (0, 0), fx=cell_size+sz/150, fy=cell_size+sz/150)
                cv2.imwrite(icon_name, dst)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

# scale_percent is the percent of original size
def resize_food(scale_percent):
    img = cv2.imread("src/images/algea2.png", cv2.IMREAD_UNCHANGED)
    print('Original Dimensions : ',img.shape)
    
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    print('Resized Dimensions : ', resized.shape)
    cv2.imwrite("src/newUI/images/small_food.png", resized)
    
    cv2.imshow("Resized image", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

create_db()
# resize_food()
