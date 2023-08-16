# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал),
# и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/homework')
def homework():
    context = {'title': 'Онлайн магазин'}

    return render_template('HW1.html', **context)


@app.route('/cloth/')
def cloth():
    context = {'title': 'Одежда'}
    return render_template('Одежда.html', **context)


@app.route('/shoes/')
def shoes():
    _data = [{"бренд": 'nike'},
             {"цена": 5000},
             {"размеры": 's,m,l'}
             ]
    context = {
        'title': 'Обувь',
        'data': _data
    }
    return render_template('Обувь.html', **context)


@app.route('/jacket/')
def jacket():
    _data = [{"бренд": 'adidas'},
             {"цена": 10000},
             {"размеры": 'xs, s, l'}
             ]
    context = {'title': 'Куртка',
               'data':_data}
    return render_template('Куртка.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
