Exam_Bengali = int (input("Bangla: "))
Exam_Enlish = int (input("English: "))
Exam_Math = int (input("Mathematics: "))
Exam_Science = int (input("Science: "))
Exam_HSS = int (input("Historical and social science: "))
Exam_DT = int (input("Digital Technology: "))
Exam_LL = int (input("Life and Liveliness: "))
Exam_AC = int (input("Art and Culture: "))
Exam_WB = int (input("Wellbeing: "))
Exam_Relg = int (input("Religion: "))

Total_Bengali = (Exam_Bengali*70/100)+30
Total_Enlish = (Exam_Enlish*70/100)+30
Total_Math = (Exam_Math*70/100)+30
Total_Science = (Exam_Science*70/100)+30
Total_HSS = (Exam_HSS*70/100)+30
Total_DT = (Exam_DT*70/100)+30
Total_LL = (Exam_LL*70/100)+30
Total_AC = (Exam_AC*70/100)+30
Total_WB = (Exam_WB*70/100)+30
Total_Relg = (Exam_Relg*70/100)+30
      
Total = Exam_Bengali+ Exam_Enlish+Exam_Math+Exam_Science+Exam_HSS+Exam_DT +Exam_LL+Exam_AC +Exam_WB+ Exam_Relg
Grand_Total = (Total*70/100)+300
       
Percentage = Total/10
Total_Percentage = Grand_Total/10

print ("                                       ")
print ("Your marks of final exam are -")
print ("Bangla: ", Exam_Bengali)
print ("English: ", Exam_Enlish)
print ("Mathematics: ", Exam_Math)
print ("Science: ", Exam_Science)
print ("Historical and Social Science: ", Exam_HSS)
print ("Digital Technology: ", Exam_DT)
print ("Life and Liveliness: ", Exam_LL)
print ("Art and Culture: ", Exam_AC)
print ("Wellbeing: ", Exam_WB)
print ("Religion: ", Exam_Relg)

print ("                                       ")
print ("Your converted marks are -")
print ("Bangla: ", Total_Bengali)
print ("English: ", Total_Enlish)
print ("Mathematics: ", Total_Math)
print ("Science: ", Total_Science)
print ("Historical and Social Science: ", Total_HSS)
print ("Digital Technology: ", Total_DT)
print ("Life and Liveliness: ", Total_LL)
print ("Art and Culture: ", Total_AC)
print ("Wellbeing: ", Total_WB)
print ("Religion: ", Total_Relg)

print ("                                       ")
print ("Total: ", Total)
print ("Percentage: ", Percentage)
print ("Converted Total: ", Grand_Total)
print ("Percentage: ",Total_Percentage)

if Total_Percentage >= 80:
    print ("Grade: A+")
elif Total_Percentage >= 70:
    print ("Grade: A")
elif Total_Percentage >= 60:
    print ("Grade: B")
elif Total_Percentage >= 50:
    print ("Grade: C")
elif Total_Percentage >= 40:
    print ("Grade: D")
else:
    print ("Grade: F")
