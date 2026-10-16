class Univariate:
    def get_Quan_Qual(self,source):
        qual=[]
        quan=[]
        for col in source.columns:
            if(source[col].dtypes == 'O'):
                qual.append(col)
            else:
                quan.append(col)
    
        return qual,quan
