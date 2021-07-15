## Approach

Using Google Earth, **104** simulated paths are created in the surrounding region of Cottage Grove Parking Garage at 
UNLV.


!!! tip "Strengthening Real Data With Created Data"
    
    In a real life scenario, it is expected that coordinate data for training the model would come from actual user 
    data that is collected around the region of the parking garage. Because of the ease of creating new paths around 
    the region of a parking garage in google earth, it is possible to strengthen the accuracy of a model that is being 
    trained using only real data. 

!!! info "All Simulated Paths"

    ![All](https://user-images.githubusercontent.com/56806733/123881389-681b2d80-d8f9-11eb-8f5a-8c2b66428802.png)

Each path contains 20 coordinates, and is labeled in the dataset for if the path enters the garage, or doesn't enter 
the garage. 

## Garage Layout

!!! example "Garage Layout"

    There are 4 main entrances to the garage labeled by the markers *A*, *B*, *C*, *D*. Furthermore there is a 
    unique location known as the *Box Office* adjacent to the garage that is labeled. The labels for the garage are 
    included only for easier tracking of the paths - in a real life data collection scenario this would not be 
    important.
    
    ![Just_Garage_Labeled](https://user-images.githubusercontent.com/56806733/123877346-e247b400-d8f1-11eb-85d2-49f92b11c4a5.png)

## Distributions of Paths

!!! info "Important"

    Since the paths are simulated, they do not accurately represent the proper distribution of traffic in the region 
    outside of this particular garage. With real data collection, the distribution and traffic of certain paths 
    would be captured and enhance the accuracy of the trained model. 

!!! list "Distributions"

     |  Location  | Entered Garage | Missed Garage |
    |:----------:|:--------------:|:-------------:|
    |      A     |       25       |       20      |
    |      B     |       22       |       16      |
    |      C     |        9       |       2       |
    |      D     |        3       |       1       |
    | Box Office |        0       |       6       |
    |    Total   |       59       |       45      |
    
!!! example "Images"

    === "Location A"

        ??? Success "Entered Garage"

            ![A_Entered](https://user-images.githubusercontent.com/56806733/123879296-8c750b00-d8f5-11eb-9130-2c2d4f5a497f.png)

        ??? Failure "Missed Garage"

            ![A_Missed](https://user-images.githubusercontent.com/56806733/123880270-24bfbf80-d8f7-11eb-8bfb-d7fa202a17e3.png)

    === "Location B"

        ??? Success "Entered Garage"

            ![B_Entered](https://user-images.githubusercontent.com/56806733/123880529-b7605e80-d8f7-11eb-9df6-b4ea862cde68.png)

        ??? Failure "Missed Garage"

            ![B_Missed](https://user-images.githubusercontent.com/56806733/123880730-2342c700-d8f8-11eb-9d25-8f45f013b23e.png)

    === "Location C"

        ??? Success "Entered Garage"

            ![C_Entered](https://user-images.githubusercontent.com/56806733/123880915-7e74b980-d8f8-11eb-9b5f-0263b954630e.png)

        ??? Failure "Missed Garage"

            ![C_Missed](https://user-images.githubusercontent.com/56806733/123881038-b976ed00-d8f8-11eb-90b9-058d643de5f0.png)

    === "Location D"

        ??? Success "Entered Garage"

            ![D_Entered](https://user-images.githubusercontent.com/56806733/123881092-db706f80-d8f8-11eb-8f11-11ecb26faae0.png)

        ??? Failure "Missed Garage"

            ![D_Missed](https://user-images.githubusercontent.com/56806733/123881157-fe028880-d8f8-11eb-8352-493d44637b5b.png)

    === "Location Box Office"

        ??? Failure "Missed Garage"

            ![BoxOffice_Missed](https://user-images.githubusercontent.com/56806733/123881317-44f07e00-d8f9-11eb-8f97-0432e619239b.png)
