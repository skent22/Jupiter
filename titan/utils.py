import matplotlib.pyplot as plt
from io import BytesIO
import base64
from titan.models import drug, prescriber, state, credential


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_top_opioid(x, y):
    plt.switch_backend('AGG')
    plt.title('Top Opioid Prescriptions', fontsize=20)
    New_Colors = ['green','blue','purple','brown','teal']
    plt.bar(x, y, color=New_Colors)
    #plt.xlabel('Opioid', fontsize=14)
    plt.ylabel('Prescriptions Filled', fontsize=10)
    plt.xticks(rotation=30)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_top_prescriptions(x, y):
    plt.switch_backend('AGG')
    plt.title('Top Prescriptions', fontsize=20)
    New_Colors = ['green','blue','purple','brown','teal', 'red', 'yellow', 'grey', 'black', 'orange']
    plt.bar(x, y, width=0.25, color=New_Colors, edgecolor='grey')
    plt.xlabel('Prescriber', fontsize=14)
    plt.ylabel('Prescriptions Filled', fontsize=10)
    plt.xticks(rotation=30)
    #plt.tight_layout()
    graph = get_graph()
    return graph
