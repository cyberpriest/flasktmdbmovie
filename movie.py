from flask import Flask ,render_template,jsonify,url_for,request
import requests

app = Flask(__name__)
app.config['SECRET_KEY']  = '12342123432'


@app.route('/search')
def Search():
	api_key = 'ba9dd7864b71ce6d54fa8b1631a49b6d'
	
	get_data = request.args.get('query')


	if not get_data :
		return jsonify({'error': 'Missing query parameter'}), 400
	url = 'https://api.themoviedb.org/3/search/movie?query={0}&api_key={1}'
	req = requests.get(url.format(get_data,api_key))
	data = req.json().get('results',[])
	response = {'search':data}

	return jsonify(response)




@app.route('/')
def home():
	



	return render_template('home.html')


@app.route('/movie/details/<int:ids>')
def movie_details(ids):
	
	id_detail = 'https://api.themoviedb.org/3/movie/{0}?api_key=ba9dd7864b71ce6d54fa8b1631a49b6d'
	r = requests.get(id_detail.format(ids))
	response  = r.json()

	if ' status_code ' in response and response['status_code'] == 34 :
		return jsonify({'error':'not found'}) , 404

	return render_template('movie_details.html',movie=response)

	# return render_template('movie_details.html',movie=response)


@app.route('/movielist')
def MovieList():
	api_key = 'ba9dd7864b71ce6d54fa8b1631a49b6d'
	page = request.args.get('page',1)
	per_page = 10 
	url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={0}&api_key={1}"
	headers = {
	    "accept": "application/json",
	}
	response = requests.get(url.format(page,api_key), headers=headers)
	r  = response.json().get('results',[])
	sorted_movies = sorted(r, key=lambda x: x.get('release_date'), reverse=True)
	response_data = {'category': 'Upcoming', 'movies': sorted_movies}
	if response.status_code == 200 :
		return jsonify(response_data)
	else : 
		return jsonify({'error': 'Failed to fetch  up coming movies'}), response.status_code





	









if __name__ == '__main__':
	app.run(debug=True)