def chunks(lst, n):
    """
    Copypaste from https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    Yield successive n-sized chunks from lst.
    """
    for i in range(0, len(lst), n):
        yield i, lst[i:i + n]