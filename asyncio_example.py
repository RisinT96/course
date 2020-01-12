import asyncio


async def find_divisibles(inrange, div_by):
    print(f'finding nums in range {inrange} divisible by {div_by}')
    located = []
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
        if i % 500000 == 0:
            await asyncio.sleep(0.01)
            # import time
            # time.sleep(0.01)

    print(f'done w/ nums in range {inrange} divisible by {div_by}')
    return located


async def main():
    loop = asyncio.get_event_loop()
    divs1 = loop.create_task(find_divisibles(50800000, 34113))
    divs2 = loop.create_task(find_divisibles(100052, 3210))
    divs3 = loop.create_task(find_divisibles(500, 3))
    # import time
    # time.sleep(10)
    await asyncio.wait([divs1, divs2, divs3])
    # async with loop.create_server() as server:
    #    pass
    return divs1, divs2, divs3


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    d1, d2, d3 = loop.run_until_complete(main())
    print(d1.result())
    print(d2.result())
    print(d3.result())
