def cosine_fun(document):
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(document)
    from sklearn.metrics.pairwise import cosine_similarity
    l=list()
    l=cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[0:2])
    return l[0][1]
import pandas as pd
df=pd.read_csv('sample.csv')
df['dob'] =pd.to_datetime(df.dob)
df=df.sort_values(['dob','fn','gn','ln'])
x=len(df)
df=df.reset_index(drop=True)
print df
l=list()
m=list()
for i in range(0,x):
    m.append(0)
for ind, row in df.iterrows():
    if ind==0:
        m[ind]=1
        l.append(ind)
        continue
    if df['dob'][ind]==df['dob'][ind-1] and df['gn'][ind]==df['gn'][ind-1]:
        s1 = df['fn'][ind]
        s2 = df['fn'][ind - 1]
        d = (s1, s2)
        f = cosine_fun(d)
        y=len(l)
        j=l[y-1]
        s1 = df['fn'][ind]
        s2 = df['fn'][j]
        d = (s1, s2)
        g = cosine_fun(d)
        if f<g:
            f=g
        if df['fn'][ind].startswith(df['fn'][ind-1]) or df['fn'][ind]==df['fn'][ind-1] or f>0.55:
            s1=df['ln'][ind]
            s2=df['ln'][ind-1]
            d=(s1,s2)
            f=cosine_fun(d)
            y = len(l)
            j = l[y - 1]
            s1 = df['ln'][ind]
            s2 = df['ln'][j]
            d = (s1, s2)
            g = cosine_fun(d)
            if f < g:
                f = g
            if df['ln'][ind].startswith(df['ln'][ind-1]) or df['ln'][ind]==df['ln'][ind-1] or f>0.55:
                if m[ind-1]==0:
                    m[ind-1]=1
                    m[ind]=1
                    l.append(ind-1)
                else:
                    m[ind]=1
            else:
                m[ind]=1
                l.append(ind)
        else:
            m[ind] = 1
            l.append(ind)
    else:
        m[ind] = 1
        l.append(ind)
c=0
for i in l:
    c=c+1
print 'Deduplicated number of names:'
print c
df['dob'] = df['dob'].dt.strftime('%d/%m/%y')
import csv
with open('changed.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_NONE)
    spamwriter.writerow(['ln']+['dob']+['gn']+['fn'])
    for i in l:
        spamwriter.writerow([df['ln'][i]]+[df['dob'][i]]+[df['gn'][i]]+[df['fn'][i]])