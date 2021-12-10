#for nodename in root node1 node2 node3 node4;
#do
#       python3 node.py $nodename network1 &
#       if ["$nodename" == "root"]; then
#               rootid = $!
#       fi
#done

#sleep 30s
#echo "-----!!!!$rootid!!!------"
#kill $rootid


# Run a a p2p network of 5 nodes 
python3 node.py root $1 &
rootid=$!
python3 node.py node1 $1 &
node1id=$!
python3 node.py node2 $1 &
node2id=$!
python3 node.py node3 $1 &
node3id=$!
python3 node.py node4 $1 &
node4id=$!

sleep 30s

# Demonstrate root node failure
kill $rootid

# After 5 minutes stop the p2p network
sleep 5m

kill $node1id
kill $node2id
kill $node3id
kill $node4id