import xlwt
import numpy

class ResultHandler:
    def __init__(self, classes):
        self.__id = 0
        self.classes_ = classes
        self.__results = []
        self.__separator = ';'

    def add_result(self, prediction_vector, correct_result):
        self.__results.append((correct_result, prediction_vector))

    def error_rate(self):
        nb_correct = 0
        nb_all = len(self.__results)
        for i in range(0,len(self.__results)):
            if self.__is_correct(i):
                nb_correct += 1
        error_rate = (nb_all - nb_correct)/nb_all
        return error_rate * 100

    def write_results_to_excel_file(self, filename, sheet):
        # Create a file
        book = xlwt.Workbook()
        sh = book.add_sheet(sheet)
        # Write the header (Correct result, classes' names)
        header = ['Lp.', 'Correct result']
        for class_ in self.classes_:
            header.append(str(class_))
        header.append("Is correct")

        for n,column_title in enumerate(header):
            sh.write(0,n,column_title)

        # Write the results
        for i in range (1,len(self.__results) + 1):
            sh.write(i,0,i)
            result = self.__results[i-1]
            sh.write(i,1,result[0])
            for j in range (2,len(result[1]) + 2):
                sh.write(i,j,result[1][j-2])
            sh.write(i,len(self.classes_)+2, self.__is_correct(i-1))

        # Calculate and add error rate to the file - optional
        # Save the file
        if (filename.endswith('.xlsx')):
            filename = filename[:len(filename)-1]
        if not (filename.endswith('.xls')):
            filename += '.xls'

        last_index = len(self.__results) + 1
        sh.write(last_index,0,"%Error rate")
        sh.write(last_index,1,self.error_rate())

        book.save(filename)

    def __is_correct(self, index):
        (correct_result, prediction_vector) = self.__results[index]
        #prediction = self.classes_[prediction_vector.index(max(prediction_vector))]
        prediction = self.classes_[numpy.where(prediction_vector == max(prediction_vector))]
        if prediction == correct_result:
            return True
        else:
            return False
