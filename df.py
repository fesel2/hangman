import pandas as pd
x_coordinates = [450,500,550,600, 450,500,550,600, 450,500,550,600, 450,500,550,600, 450,500,550,600, 450,500,550,600, 450,500]
y_coordinates = [150,150,150,150, 200,200,200,200, 250,250,250,250, 300,300,300,300, 350,350,350,350, 400,400,400,400, 450,450]
letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
button_names = ["button"+str(i) for i in range(26)]

df = pd.DataFrame({"x":x_coordinates, "y":y_coordinates, "letter": letters, "name": button_names})
print(df)
df.to_csv("alphabet.csv", index=False, )