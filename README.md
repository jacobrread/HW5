# HW5: Game Theory

## Console Args
Usage: python Game.py <strategy> <version>
Available strategies are 'Dove' and 'Hawk'
Available versions are 'Vanilla' and 'Modified'

Strategies indicate what type of creatures will be included in the simulation. Dove only includes doves while Hawk includes hawks and doves. 

Versions indicate the type of simulation. Vanilla encompasses the youtube video situation while Modified implements part two of the homework. 

Example input: python Game.py Hawk Modified

This would run the simulation with hawks and it would use the modified scenario described in part two of the homework.

## Comment on the emergent behaviors. What is the difference you see in the populations at "equilibrium"?
An average run has results similar to this:

Strategy: Dove
Version: Vanilla
Total doves: 72
Total hawks: 0
Average doves: 63.74
Average hawks: 0.0

Strategy: Hawk
Version: Vanilla
Total doves: 34
Total hawks: 15
Average doves: 39.95
Average hawks: 18.97

Strategy: Dove
Version: Modified
Total doves: 64
Total hawks: 0
Average doves: 63.75
Average hawks: 0.0

Strategy: Hawk
Version: Modified
Total doves: 63
Total hawks: 43
Average doves: 58.98
Average hawks: 34.88

If you look at these four means you can see that the average amount of doves with no hawks is virtually the same. Things differ between the two hawk simulations as the overall population is larger in the modified version vs the vanilla version. Additionally, the both the total doves and total hawks are larger in the modified than in the vanilla version.

What surprised me was that the 'Hawk Modified' has extremely varying results. Sometimes the hawk population exceeds the dove population in only 100 days. Other times it never gets above a fourth of the dove population in the 100 days. 

