import json

with open('outputs/working/batch_1_fragment.json') as f:
    data = json.load(f)

with open('outputs/working/batch_1_ids.json') as f:
    batch_ids = set(json.load(f))

# Filter links
new_links = []
removed_link_indices = set()
for i, link in enumerate(data['links']):
    link_mids = set(link['matrix_ids'])
    if link_mids.issubset(batch_ids):
        new_links.append(link)
    else:
        removed_link_indices.add(i)
        print('Removing link[{}]: {}'.format(i, link['matrix_ids']))

# Remap link indices for atomic_links
old_to_new = {}
new_idx = 0
for old_idx in range(len(data['links'])):
    if old_idx not in removed_link_indices:
        old_to_new[old_idx] = new_idx
        new_idx += 1

# Filter atomic_links
new_atomic = []
for al in data['atomic_links']:
    if al['matrix_id'] in batch_ids:
        if al['link_index'] is not None:
            if al['link_index'] in removed_link_indices:
                print('Removing atomic: {} <-> {} (link removed)'.format(al['matrix_id'], al['contract_id']))
                continue
            al['link_index'] = old_to_new[al['link_index']]
        new_atomic.append(al)

# Filter unmatched
new_unmatched = [um for um in data['unmatched_matrix'] if um['matrix_id'] in batch_ids]

data['links'] = new_links
data['atomic_links'] = new_atomic
data['unmatched_matrix'] = new_unmatched

with open('outputs/working/batch_1_fragment.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Links: {}, Atomic: {}, Unmatched: {}'.format(len(new_links), len(new_atomic), len(new_unmatched)))
