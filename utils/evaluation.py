def get_pcf_rank(ranked_list, target_omim):
    count = 1
    for diagnosis in ranked_list:
        suggested_omim = diagnosis['id'].replace('OMIM:', '')
        if suggested_omim == str(target_omim):
            break
        count += 1

    return count

def get_gm_rank(ranked_list, target_omim):
    count = 1
    for diagnosis in ranked_list:
        suggested_omim = diagnosis['omim_id']
        if suggested_omim == target_omim:
            break
        count += 1

    return count
