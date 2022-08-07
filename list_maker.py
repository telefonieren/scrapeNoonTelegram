import os
import json
import random
import time
id = 1

def collect_all_items(id):
    init_collection = []
    directory = os.getcwd()
    print(directory)
    for file in os.listdir(directory+'\\'):
        if file.endswith('.json') and not file.endswith('collection.json'):
            print(os.path.join('', file))
            with open(file) as ifile:
                print(f'opened {file}')
                goods = json.load(ifile)
                for good in goods:

                    good['id']=id
                    id += 1
                    # time.sleep(0.1)
                    init_collection.append(good)
            ifile.close()
    return id

    with open('collection.json', 'w') as jsonfile:
        json.dump(init_collection, jsonfile, indent=4, ensure_ascii=False)
    jsonfile.close()


def create_day_list(id):

    ids = random.sample(range(1,id),36)
    print(ids)
    final_result = []
    for element in ids:
        with open('collection.json') as file:
            goods = json.load(file)
            for good in goods:
                cid = good.get('id')
                if cid == element:
                    print(good.get('title'))
                    final_result.append(
                        {
                            'title':good.get('title'),
                            'discount': good.get('discount'),
                            'old_price': good.get('old_price'),
                            'new_price': good.get('new_price'),
                            'link': good.get('link')
                        }
                    )
        file.close()
    with open('final_result.json', 'w') as jfile:
        json.dump(final_result, jfile, indent=4, ensure_ascii=False)
    jfile.close()

def main():
    pid = collect_all_items(id)
    create_day_list(pid)

if __name__ == '__main__':
    main()
