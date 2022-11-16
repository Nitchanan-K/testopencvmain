'''        
    def find(self, base_img, threshold = 0.96,max_results=10):
        # run opencv algorithm
        result = cv2.matchTemplate(base_img, self.obj_img, self.method)

        # locations found with >= threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # if we found no results, return now. this reshape of the empty array allows us to 
        # concatenate together results without causing an error
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # fisrt make list fo [x , y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.obj_w, self.obj_h]
            # append it twice to make sure that it overlap
            rectangles.append(rect)
            rectangles.append(rect)

        # gourping rectagles
        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
        # print(rectangles)

        # for performance reasons, return a limited number of results.
        # these aren't necessarily the best results.
        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles
'''