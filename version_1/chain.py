import base_blockchain

# Contains everything building the blockchain related

blockchain = base_blockchain.BlockChain()

def create_block(circle):
    last_block = blockchain.latest_block
    last_proof_no = last_block.proof_no
    proof_no = blockchain.proof_of_work(last_proof_no)
    block_data = blockchain.new_data(
        name = circle.name,
        timestep = circle.timestep,
        collected_amt = circle.collected_amt,
        balance = circle.balance,
        data = circle.data
    )

    last_hash = last_block.calculate_hash
    block = blockchain.construct_block(proof_no, last_hash)

    new_block = blockchain.latest_block
    new_hash = new_block.calculate_hash
    print("Added block: " + str(block.index) + ", hash - " + str(new_hash) + ", prev_hash - " + str(block.prev_hash) + ", timestep - " + str(circle.timestep))

    return block
