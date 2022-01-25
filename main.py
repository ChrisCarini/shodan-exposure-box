import math

from shodan import get_port_bars, get_port_data, get_shodan_exposure_data, update_gist


def main():
    locale = 'US'
    data = get_shodan_exposure_data(locale=locale)

    min_count, max_count, total = get_port_data(data)

    min_order_of_magnitude = int(f'1{"0" * math.floor(math.log(min_count, 10))}')
    max_order_of_magnitude = int(f'1{"0" * math.floor(math.log(max_count, 10))}')

    print(f'Locale                : {locale}')
    print(f'Min                   : {min_count}')
    print(f'Max                   : {max_count}')
    print(f'Min order of magnitude: {min_order_of_magnitude}')
    print(f'Max order of magnitude: {max_order_of_magnitude}')
    print()
    print('        10        20        30        40        50  54')
    print('123456789012345678901234567890123456789012345678901234')

    update_gist(
        title=f'Shodan.io Port Usage - {locale}',
        content=get_port_bars(data, max_count),
    )


if __name__ == '__main__':
    import time

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f'{__file__} executed in {elapsed:0.2f} seconds.')
