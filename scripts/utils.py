def moving_average(values:list = []) -> list:
    """Interpolate the data of the laps 
    with an ARMA process of coefficients
    [.2, .3, .5]
    
    Args:
        values (list): lap times

    Returns:
        res (list): interpolated lap times 
    """
    res = []
    res.append(values[0])
    res.append(0.3*values[0]+0.7*values[1])
    for i in range(len(values)-2):
        res.append(0.2*values[i]+0.3*values[i+1]+0.5*values[i+2])
    return res