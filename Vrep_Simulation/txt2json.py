import xml.etree.ElementTree as ET
from collections import defaultdict
import json
import argparse

parser = argparse.ArgumentParser(description='txt to json converter')
# parser.add_argument('-i', '--input', type=str, help='text file name')
# parser.add_argument('-o', '--output', type = str, help ='save json file name', default='result.json')
args = parser.parse_args()

# Directory: 사용자에 맞춰 변경
# xml_data = './results/' + args.input   # Linkage 저장 파일 경로
# result = './results/' + args.output      # json 변환 파일 저장 경로
xml_data = './results/Untitled.txt' #+ args.input   # Linkage 저장 파일 경로
result = './results/1030_test.json' #+ args.output      # json 변환 파일 저장 경로

# --------------------------------------여기부턴 수정 x -----------------------------------------------
json_blank = 'blank.json'

# data.txt 파일에서 XML 데이터 읽기
with open(xml_data, 'r') as file:
    tree = ET.parse(file)

root = tree.getroot()

# connector 태그의 내용 추출
connectors = []
for connector in root.findall('connector'):
    attributes = connector.attrib
    connectors.append(attributes)

# Link 태그의 내용 추출
links = []
for link in root.findall('Link'):
    link_data = {
        "attributes": link.attrib,
        "connectors": [connector.get('id') for connector in link.findall('connector')]
    }
    links.append(link_data)

# XML에서 Point 좌표, 특성 추출
points_dict = defaultdict(list)
anchor_dict = defaultdict(list)
motor_dict = defaultdict(list)
marker_dict = defaultdict(list)


for connector in connectors:
    if 'anchor' in connector.keys():
        if 'input' in connector.keys():
            motor_dict['{}'.format(connector['id'])] = {
                                                    "x": '{:.2f}'.format(float(connector['x'])),
                                                    "y": '{:.2f}'.format(float(connector['y'])),
						                            "z": "0.00"
                                                        }
        anchor_dict['{}'.format(connector['id'])] = {
                                                "x": '{:.2f}'.format(float(connector['x'])),
                                                "y": '{:.2f}'.format(float(connector['y'])),
                                                "z": "0.00"
                                                    }
    points_dict['{}'.format(connector['id'])] = {
                                            "x": '{:.2f}'.format(float(connector['x'])),
                                            "y": '{:.2f}'.format(float(connector['y'])),
                                            "z": "0.00"
                                                }
    if connector['selected'] == 'true':
        marker_dict['{}'.format(connector['id'])] = {
                                            "x": '{:.2f}'.format(float(connector['x'])),
                                            "y": '{:.2f}'.format(float(connector['y'])),
                                            "z": "0.00"
                                                }
# Anchor 정의
anc_dict = dict()
anc_dict['points'] = list(anchor_dict.values())

# Link 정의
link_dict = list()

for link in links:
    link_dict.append({
				"name": "Link{}".format(link['attributes']['id']),
				"points": [
					points_dict['{}'.format(link['connectors'][0])],
					points_dict['{}'.format(link['connectors'][1])]
				]
			})
    
# Constraints 정의
const_dict = list()

for idx, p in points_dict.items():
    const = {
				"name": f"CoaxialConstraint{idx}",
				"points": list()
			}
    for l in link_dict:
        if p in l['points']:
            targetpoint = {
                        "targetLink": "{}".format(l['name']),
                        "targetIndex": l['points'].index(p)
                    }
            const['points'].append(targetpoint)
        
        
    if idx in anchor_dict.keys():
        targetpoint = {
                    "targetLink": "Anchor",
                    "targetIndex": list(anchor_dict.values()).index(p)
                }
        const['points'].append(targetpoint)
        
    const_dict.append(const)

# Markers 정의
if list(marker_dict.keys()):
    temp = list()
    for m in marker_dict.keys():

        for n in const_dict:
          if m in n['name']:
            temp.append(n['points'][0])
    marker_dict = temp
else:
    raise ValueError('Please specify the marker')

# Motor 정의
if list(motor_dict.keys()):
    temp = list()
    for idx, m in enumerate(motor_dict.keys()):
        for n in const_dict:
            linklst = list()
            if m in n['name']:
                for l in n['points']:
                    linklst.append(l['targetLink'])
                m_dict = {
                        "name": f"Motor{idx+1}",
                        "targetConstraint": "{}".format(n['name']),
                        "type": "DC",
                        "direction": 0,
                        "speed": 100,
                        "phase": 0,
                        "range": "0-180"
                    }
                for i, t in enumerate(linklst):
                    m_dict['targetLink{}'.format(i+1)] = t
        temp.append(m_dict)
    motor_dict = temp
else:
    raise ValueError('Please specify the motor')

# json 저장
# JSON 파일을 읽기 모드로 열고, 내용을 data 변수에 저장
with open(json_blank, 'r') as json_file:
    data = json.load(json_file)

data['sketch']['anchor'] = anc_dict
data['sketch']['constraints'] = const_dict
data['sketch']['links'] = link_dict
data['sketch']['markers'] = marker_dict
data['sketch']['motors'] = motor_dict

with open(result, 'w') as json_file:
    json.dump(data, json_file, indent=4)