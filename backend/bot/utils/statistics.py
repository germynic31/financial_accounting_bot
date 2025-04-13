from io import BytesIO

import matplotlib.pyplot as plt


async def generate_pie_chart(expenses: dict) -> BytesIO:
    """Генерирует "пирог" со статистикой трат."""
    labels = list(expenses.keys())
    sizes = list(expenses.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Круговая диаграмма

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer
