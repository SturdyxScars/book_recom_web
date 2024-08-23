from flask import Flask, render_template, request
import pickle
import numpy as np

top_df = pickle.load(open('templates/popular.pkl', 'rb'))
books = pickle.load(open('book_df.pkl', 'rb'))
pv = pickle.load(open('pv.pkl', 'rb'))
similar = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           names=list(top_df['title'].values),
                           image=list(top_df['url'].values),
                           votes=list(top_df['num_rating'].values),
                           author=list(top_df['author'].values),
                           rating=list(top_df['av.rating'].round())
                           )


@app.route('/recom')
def recom():
    return render_template('recom.html')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_inp = request.form.get('user_inp')
        data = []
        if user_inp in pv.index:
            ind = np.where(pv.index == user_inp)[0][0]
            sorts = sorted(enumerate(similar[ind]), key=lambda x: x[1], reverse=True)[1:6]
            for i in sorts:
                inp = []
                temp = books[books['title'] == pv.index[i[0]]]
                temp.drop_duplicates('title', inplace=True)
                inp.extend((temp['title'].values).tolist())
                inp.extend((temp['author'].values).tolist())
                inp.extend((temp['url'].values).tolist())

                data.append(inp)
        print(data)

        return render_template('recom.html', data=data)

    return render_template('recom.html')

if __name__ == '__main__':
    app.run(debug=True)
