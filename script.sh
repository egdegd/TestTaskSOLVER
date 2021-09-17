input_len=$(python3 circuit_sat_to_sat.py circuit_sat.bench)
cadical/build/cadical -q formula.cnf | sed -n '1p'
cadical/build/cadical -q formula.cnf | sed -n '2p' | awk -F "$input_len" '{print $1}'