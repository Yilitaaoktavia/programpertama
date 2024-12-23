from flask import Flask, jsonify, request, make_response
from model import Data

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def hello():
    data = [{
        'nama': 'Galih',
        'pekerjaan': 'Web Engineer',
        'pesan': 'Hello Lita'
    }]
    return make_response(jsonify({'data': data}), 200)


@app.route('/karyawan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def karyawan():
    try:
        # Memanggil class model database
        dt = Data()
        values = ()

        # Jika Method GET
        if request.method == 'GET':
            id_ = request.args.get("id")
            if id_:
                query = "SELECT * FROM data_karyawan WHERE id = %s"
                values = (id_,)
            else:
                query = "SELECT * FROM data_karyawan"
            data = dt.get_data(query, values)

        # Jika Method POST
        elif request.method == 'POST':
            datainput = request.json
            nama = datainput['nama']
            pekerjaan = datainput['pekerjaan']
            usia = datainput['usia']

            query = "INSERT INTO data_karyawan (nama, pekerjaan, usia) VALUES (%s, %s, %s)"
            values = (nama, pekerjaan, usia)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'Berhasil menambah data'
            }]

        # Jika Method PUT
        elif request.method == 'PUT':
            datainput = request.json
            id_ = datainput.get('id')
            if not id_:
                return make_response(jsonify({'error': 'ID harus disertakan untuk update'}), 400)

            # Membangun query dan values dinamis
            query = "UPDATE data_karyawan SET "
            updates = []
            values = []

            if 'nama' in datainput:
                updates.append("nama = %s")
                values.append(datainput['nama'])
            if 'pekerjaan' in datainput:
                updates.append("pekerjaan = %s")
                values.append(datainput['pekerjaan'])
            if 'usia' in datainput:
                updates.append("usia = %s")
                values.append(datainput['usia'])

            if not updates:
                return make_response(jsonify({'error': 'Tidak ada data untuk diupdate'}), 400)

            query += ", ".join(updates) + " WHERE id = %s"
            values.append(id_)

            dt.insert_data(query, tuple(values))
            data = [{
                'pesan': 'Berhasil mengubah data'
            }]

        # Jika Method DELETE
        elif request.method == 'DELETE':
            id_ = request.args.get("id")
            if not id_:
                return make_response(jsonify({'error': 'ID harus disertakan untuk delete'}), 400)

            query = "DELETE FROM data_karyawan WHERE id = %s"
            values = (id_,)
            dt.insert_data(query, values)
            data = [{
                'pesan': 'Berhasil menghapus data'
            }]

        # Selain itu, metode tidak diizinkan
        else:
            return make_response(jsonify({'error': 'Method tidak diizinkan'}), 405)

    except Exception as e:
        # Menangkap error dan memberikan pesan error yang sesuai
        return make_response(jsonify({'error': str(e)}), 400)

    # Mengembalikan data dalam response JSON
    return make_response(jsonify({'data': data}), 200)


if __name__ == "__main__":
    app.run()
