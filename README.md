# Scalable Computing Project 3: Poacher Detection with Drones

We have built a peer-to-peer network to detect illegal hunting of animals in national parks, usually referred to as poaching. Poaching can be detected with the help of a network of drones, which will be the nodes or peers of the network. The park ranger operates on one of the nodes, which we call the root node. Each drone sends spatial information of a specific area of the park to the root node. The root node in turn inspects the information for presence of a poacher with the help of deep learning algorithms. If a poacher is detected, an alert is raised.

# Bash Script to run the network

The following bash scripts will instantiate a network on P2P nodes on each of the two PI's. We can see how the nodes in the network discover each other nodes & how the sensors continuously send data to the nodes. If a poacher is seen, the system will alert the root node which will communicate this information across networks through gateway nodes. 

The script also demonstrates how we handle the failure of root node by purposefully killing the node after 1 minute of starting the network. We can see that the network uses a 180 seconds timeout for declaring the node as dead and then elects a new root node. The script also brings down the full network after 10 minutes as a closure activity.

## Run the following command on the first PI

```./runme.sh network1```

## Run the following command on the second PI

```./runme.sh network2```