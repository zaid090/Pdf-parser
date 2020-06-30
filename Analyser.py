import pandas as pd
import numpy as np
import tabula as tb
import os
    
class Analyser:
    def __init__(self):
        pass
        
    def PDF_parser(self,filepath):
        self.filepath = filepath
        lst = tb.read_pdf(self.filepath, pages = 'all')
        firstrun = True
        self.subject_codes = list()
        mdf = pd.DataFrame()
        total_students = 0
        for df in lst:
            nl = list()
            for j in df["Unnamed: 0"]:
                nl.append(np.NaN)
            ndf = pd.DataFrame(nl)
            df["Gender"] = ndf
            del ndf,nl
            df = df.fillna("")        
            stdcount = 0
            scount = 0
            for i in df["Unnamed: 1"]:
                if i.isdigit() and len(i) >= 6:
                    df["Unnamed: 1"].loc[stdcount] = i
                    stdcount += 1
            stdcount = 0
                
            for i in df["Unnamed: 0"]:  
                if "/" in i:
                    j = i.split("/")
                    df["Unnamed: 0"].loc[stdcount] = j[0]
                    df["Unnamed: 1"].loc[stdcount] = j[1]
                    df["Gender"].loc[stdcount] = "F"
                    scount += 1
                elif i.isdigit() and len(i) <= 4:
                    df["Gender"].loc[stdcount] = "M"
                    scount += 1
                elif " " in i and "Name of the Student" not in i and "Seat No" not in i:
                    j = i.split(" ")
                    df["Unnamed: 0"].loc[stdcount] = j[0]
                    df["Unnamed: 1"].loc[stdcount] = " ".join(j[1:])
                    df["Gender"].loc[stdcount] = "M"
                    scount += 1
                elif i.isalpha() and "Name of the Student" not in i and "Seat No" not in i:
                    df["Unnamed: 1"].loc[stdcount] = i
                    df["Unnamed: 0"].loc[stdcount] = ""
                elif i.isdigit() and len(i) >= 6:
                    df["Unnamed: 1"].loc[stdcount] = i
                    df["Unnamed: 0"].loc[stdcount] = ""

            
                stdcount += 1
            total_students += scount
            count = 0  
            for colname in df.columns:
                if("Unnamed" not in colname and " " in colname):
                    names = colname.split(" ")
                    m = len(names)
                    n = m
                    code_data = dict()
                    for i in names:
                        code_data[i] = []
                    for i in df[colname]:
                        n = m
                        for j in range(m):
                            k = i.translate({ord(k): None for k in '+*'}).split(" ")
                            k = [l for l in k if l != ""]
                            if len(k) >= 3:
                                sub = " ".join(k[:3])
                                i = " ".join(k[3:])
                            else :
                                sub = " ".join(k[:1])
                                i = " ".join(k[1:])
                            n -= 1
                            code_data[names[j]].append(sub)
                    df[colname] = code_data[names[0]]
                    df.rename(columns={colname:names[0]},inplace = True)
                    for i in range(1,len(names)):
                        df.insert(count+i,names[i],code_data[names[i]],True)
                count += 1
            if firstrun:
                mdf = df
                firstrun = False
            else:
               mdf = mdf.append(df,ignore_index=True)
        for colname in mdf.columns:
            if "Unnamed" not in colname and colname != "Gender":
                self.subject_codes.append(colname)
        self.df = mdf
        self.total_students = total_students
        return self.subject_codes
    
    
    
    # Takes Input :  Total Number of students ,DataFrame of the Data to be Analysed, A dictionary of Subject Codes : Subject Names
    # Returns Path to Analysed Data
    
    def Analysis(self, code_names = {"CSC301":"Applied Mathematics - III","CSC302":"Digital Logic Design And Analysis",
                    "CSC303":"Discrete Mathematics","CSC304":"Electronic Circuits And Communication Fundamentals",
                    "CSC305":"Data Structures","CSL301":"Digital System Lab","CSL302":"Basic Electronic Lab",
                    "CSL303":"Data Structure Lab","CSL304":"OOPM(Java)"}):
        Column_names1 = ["Sr. No.", "Seat No.", "Name","Gender"] 
        for colname in self.df.columns:
            if "Unnamed" not in colname and colname != "Gender":
                Column_names1.append(code_names[colname])
        
        Column_names1.append("SGPI")
        Column_names2 = ["","Appeared","Distinction","First Class","Second Class","Pass","With KT"]
        Column_names3 = ["Appeared","Distinction","First Class","Second Class","Pass","Fail"]
        finaldf = pd.DataFrame(columns=Column_names1,index = range(self.total_students))
        
        
        self.df = self.df.fillna("")
        
        self.AbsentM = dict(zip(code_names.keys(),[0 for i in range(len(code_names))]))
        self.AbsentF = dict(zip(code_names.keys(),[0 for i in range(len(code_names))]))
        self.Mark_ranks = ["Distinction", "First Class", "Second Class", "Pass", "Fail"]
        self.Total_rank = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        self.Total_rankM = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        self.Total_rankF = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        
        self.Sub_ranks = dict(zip(code_names.keys(),[0 for i in range(len(code_names))]))
        for sub in code_names.keys():
            self.Sub_ranks[sub] = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        
        self.Sub_ranksM = dict(zip(code_names.keys(),[0 for i in range(len(code_names))]))
        for sub in code_names.keys():
            self.Sub_ranksM[sub] = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        
        self.Sub_ranksF = dict(zip(code_names.keys(),[0 for i in range(len(code_names))]))
        for sub in code_names.keys():
            self.Sub_ranksF[sub] = dict(zip(self.Mark_ranks,[0 for i in range(len(self.Mark_ranks))]))
        
        i = j = l = ind = self.male_absent = self.female_absent = male_count = female_count = 0
        
        for col in self.df["Unnamed: 2"]:
            if col == "Maximum":
                maxi = l
            elif col == "Minimum":
                mini = l
                break
            l += 1
        for itn in self.df["Unnamed: 0"]:
            if itn.strip().isdigit() and len(itn) <= 4:
                finaldf["Sr. No."].loc[i] = itn
                finaldf["Seat No."].loc[i] = self.df["Unnamed: 1"].loc[ind + 3][-6:]
                finaldf["Name"].loc[i] = self.df["Unnamed: 1"].loc[ind]
                finaldf["Gender"].loc[i] = self.df["Gender"].loc[ind]
                finaldf["SGPI"].loc[i] = self.df["Unnamed: 6"].loc[ind + 4]
                for sub in code_names.keys():
                    if self.df[sub].loc[ind][0] == "A":
                        if self.df["Gender"].loc[ind]=="M":
                            self.AbsentM[sub] += 1
                            self.male_absent += 1
                        elif self.df["Gender"].loc[ind]=="F":
                            self.AbsentF[sub] += 1
                            self.female_absent += 1
                    else:
                        finaldf[code_names[sub]].loc[i] = self.df[sub].loc[ind].translate({ord(k): None for k in 'EF'})
                        if int(finaldf[code_names[sub]].loc[i].split(" ")[-1]) >= int(self.df[sub].loc[mini].split(" ")[-1]):     
                            marks = int(finaldf[code_names[sub]].loc[i][-3:].strip())
                            minimum = int(self.df[sub].loc[mini][-3:].strip())
                            maximum = int(self.df[sub].loc[maxi][-3:].strip())
                            if(marks >= minimum  or finaldf["SGPI"].loc[i].replace(".","").isdigit()):
                                self.Sub_ranks[sub]["Pass"] += 1
                                if finaldf["Gender"].loc[i] == "M":
                                    self.Sub_ranksM[sub]["Pass"] += 1
                                elif finaldf["Gender"].loc[i] == "F":
                                    self.Sub_ranksF[sub]["Pass"] += 1
                                if(marks >= maximum * 0.75):
                                    self.Sub_ranks[sub]["Distinction"] += 1
                                    if finaldf["Gender"].loc[i] == "M":
                                        self.Sub_ranksM[sub]["Distinction"] += 1
                                    elif finaldf["Gender"].loc[i] == "F":
                                        self.Sub_ranksF[sub]["Distinction"] += 1
                                elif(marks >= maximum * 0.6 and marks < maximum * 0.75):
                                    self.Sub_ranks[sub]["First Class"] += 1
                                    if finaldf["Gender"].loc[i] == "M":
                                        self.Sub_ranksM[sub]["First Class"] += 1
                                    elif finaldf["Gender"].loc[i] == "F":
                                        self.Sub_ranksF[sub]["First Class"] += 1
                                elif(marks >= maximum * 0.5 and marks < maximum*0.6):
                                    self.Sub_ranks[sub]["Second Class"] += 1
                                    if finaldf["Gender"].loc[i] == "M":
                                        self.Sub_ranksM[sub]["Second Class"] += 1
                                    elif finaldf["Gender"].loc[i] == "F":
                                        self.Sub_ranksF[sub]["Second Class"] += 1
                        else:
                            self.Sub_ranks[sub]["Fail"] += 1
                            if finaldf["Gender"].loc[i] == "M":
                                self.Sub_ranksM[sub]["Fail"] += 1
                            elif finaldf["Gender"].loc[i] == "F":
                                self.Sub_ranksF[sub]["Fail"] += 1
                if(self.df["Gender"].loc[ind]=="M"):
                    male_count += 1
                elif(self.df["Gender"].loc[ind]=="F"):
                    female_count += 1
                if finaldf["SGPI"].loc[i].translate({ord(k): None for k in '#.'}).isdigit():
                    pointer = float(finaldf["SGPI"].loc[i].replace("#",""))
                    if(pointer < 7 ):
                        percent = 7.1*pointer + 12
                    else:
                        percent = 7.4*pointer + 12
                    if(percent > 35):
                        self.Total_rank["Pass"] += 1
                        if finaldf["Gender"].loc[i] == "M":
                            self.Total_rankM["Pass"] += 1
                        elif finaldf["Gender"].loc[i] == "F":
                            self.Total_rankF["Pass"] += 1
                        if(percent >= 75):
                            self.Total_rank["Distinction"] += 1
                            if finaldf["Gender"].loc[i] == "M":
                                self.Total_rankM["Distinction"] += 1
                            elif finaldf["Gender"].loc[i] == "F":
                                self.Total_rankF["Distinction"] += 1
                        elif(percent >=60 and percent <75):
                            self.Total_rank["First Class"] += 1
                            if finaldf["Gender"].loc[i] == "M":
                                self.Total_rankM["First Class"] += 1
                            elif finaldf["Gender"].loc[i] == "F":
                                self.Total_rankF["First Class"] += 1
                        elif(percent >=50 and percent <60):
                            self.Total_rank["Second Class"] += 1
                            if finaldf["Gender"].loc[i] == "M":
                                self.Total_rankM["Second Class"] += 1
                            elif finaldf["Gender"].loc[i] == "F":
                                self.Total_rankF["Second Class"] += 1
                else:
                    self.Total_rank["Fail"] += 1
                    if finaldf["Gender"].loc[i] == "M":
                        self.Total_rankM["Fail"] += 1
                    elif finaldf["Gender"].loc[i] == "F":
                        self.Total_rankF["Fail"] += 1
                    
                i+=1
            ind += 1
        
        finaldf = finaldf.fillna("Absent")
        mf_countdf = pd.DataFrame(columns = Column_names1,index = range(3))
        j = 0
        lst = ["Total Student","Total Male","Total Female"]
        for i in [i,male_count,female_count]:
          mf_countdf["Name"].loc[j] = lst[j]
          mf_countdf["Gender"].loc[j] = i
          j += 1
        filldf = pd.DataFrame(columns = Column_names1,index = range(3))
        totaldf = pd.DataFrame()
        finaldf = finaldf.append(filldf, ignore_index = True)
        finaldf = finaldf.append(mf_countdf, ignore_index = True)
        
        row0 = pd.Series(Column_names2,Column_names1[2:9])
        row1 = pd.Series(["Total Student Appeared", str(self.total_students - (self.male_absent + self.female_absent))]
                                  +list(self.Total_rank.values()),Column_names1[2:9])
        row2 = pd.Series(["Total Male Student", str(male_count - self.male_absent)]
                                  +list(self.Total_rankM.values()),Column_names1[2:9])
        row3 = pd.Series(["Total Female Student", str(female_count - self.female_absent)]
                                  +list(self.Total_rankF.values()),Column_names1[2:9])
        
        totaldf = totaldf.append(row0,ignore_index=True).append(row1,ignore_index=True).append(row2,ignore_index=True).append(row3,ignore_index=True)
        finaldf = finaldf.append(filldf, ignore_index = True)
        finaldf = finaldf.append(totaldf, ignore_index = True)
        finaldf = finaldf.append(filldf, ignore_index = True)
        finaldf.loc[-1,"Name"] = "Subject Wise Result Analysis"
        finaldf = finaldf.append(filldf.iloc[1,:],ignore_index = True)
        for sub in code_names.keys():
            row0 = pd.Series([code_names[sub]]+Column_names3, Column_names1[2:9])
            row1 = pd.Series(["Total Student Appeared", str(self.total_students - (self.AbsentM[sub] + self.AbsentF[sub]))]
                                      +list(self.Sub_ranks[sub].values()),Column_names1[2:9])
            row2 = pd.Series(["Total Male Student", str(male_count - self.AbsentM[sub])]
                                      +list(self.Sub_ranksM[sub].values()),Column_names1[2:9])
            row3 = pd.Series(["Total Female Student", str(female_count - self.AbsentF[sub])]
                                      +list(self.Sub_ranksF[sub].values()),Column_names1[2:9])
            finaldf = finaldf.append(row0,ignore_index=True).append(row1,ignore_index=True).append(row2,ignore_index=True).append(row3,ignore_index=True)
            finaldf = finaldf.append(filldf, ignore_index = True)
        filename = os.path.splitext(self.filepath)[0] + " - Analysis.xlsx"
        writer = pd.ExcelWriter(filename)
        finaldf.to_excel(writer,index = False)
        writer.save()
        return filename
    
if __name__ == "__main__" :   
    #Create Analyser Object with the Path of the pdf  
    abc = Analyser()            
    codes = abc.PDF_parser("E:\\Projects\\Python Projects\\Python Tests\\SEM-III.pdf")
    #Use codes to create a dictionary of subject codes : subject name
    #Pass the created dictionary in Analysis or it will use default SE-CMPN Sem III dictionary
    filename = abc.Analysis()
    os.startfile("E:\\Projects\\Python Projects\\Python Tests\\SEM-III - Analysis.xlsx")
    #Returns the full path of the file which can be opened using os.startfile
    
