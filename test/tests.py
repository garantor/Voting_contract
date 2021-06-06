from web3 import Web3, HTTPProvider, logs


import unittest, json, secrets




class ContractTest(unittest.TestCase):
    main_address = "0xb5adee455e22e3001d1B7Ae7504723eC681AdC63" #Account from genech
    key_file = open(".secret", "r")
    main_address_privateKey = key_file.read()
    PATH_TRUFFLE_WK = '/Users/afolabi/voter_contract'
    truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/VotingContract.json'))


    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract_address  = truffleFile['networks']['5777']['address']


    web3_instantce = Web3(HTTPProvider('http://127.0.0.1:8545'))
    contract = web3_instantce.eth.contract(address=contract_address, abi= abi)
    ward = 'Oyo' + secrets.token_hex(4)
    contestants = "Alafin" + secrets.token_hex(3)

    def setUp(self) -> None:
        self.nounce = self.web3_instantce.eth.get_transaction_count(self.main_address)
        return super().setUp()

    def test_001_check_connect(self):
        connection = self.web3_instantce.isConnected()
        self.assertEqual(connection, True)
        print("Testing Connection Passed")

    def test_002_AddContestant(self):
        #Test AddContestants
        # This will crash when total user on blockchain reach max amt of 5

        add_contestants = self.contract.functions.AddContestant(self.contestants, self.ward).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce
        })

        sign_tx = self.web3_instantce.eth.account.sign_transaction(add_contestants, self.main_address_privateKey)
        send_raw_tx = self.web3_instantce.eth.send_raw_transaction(sign_tx.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(send_raw_tx)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
        event_filter = self.contract.events.contesterAdded().processReceipt(wait_for_complettion)
        self.assertTrue(event_filter[0]['args'].name == self.contestants)
        self.assertTrue(event_filter[0]['args'].ward == self.ward)
        self.assertTrue(event_filter[0]['args'].vote_count == 0)
        print("Adding Users Passed")

    # def test_003_getContestants(self):
    #     getContestants = self.contract.functions.getContestants().call()
    #     events = self.contract.events.EmitContestant().createFilter(fromBlock="latest")
    #     print(getContestants)
    #     print(events.get_all_entries())
    #     print(events.get_new_entries())

    def test_004_getIndividualContestant(self):
        getIndividualContestant =  self.contract.functions.getIndividualContestant(self.contestants).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce
        })

        sign_tx = self.web3_instantce.eth.account.sign_transaction(getIndividualContestant, self.main_address_privateKey)
        send_raw_tx = self.web3_instantce.eth.send_raw_transaction(sign_tx.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(send_raw_tx)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
        event_filter = self.contract.events.EmitInvidualContestant().processReceipt(wait_for_complettion)
        self.assertTrue(event_filter[0]['args'].name == self.contestants)
        self.assertTrue(event_filter[0]['args'].ward == self.ward)
        self.assertTrue(event_filter[0]['args'].vote_count == 0)
        print("Get indiviual contestant Passed")

    def test_005_CastVote(self):
        # This Will crash the test if the address already voted before, running the 
        # test mutiple times with same address will crash test

        CastVote = self.contract.functions.CastVote(self.contestants).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce
        })

        sign_tx = self.web3_instantce.eth.account.sign_transaction(CastVote, self.main_address_privateKey)
        send_raw_tx = self.web3_instantce.eth.send_raw_transaction(sign_tx.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(send_raw_tx)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
        event_filter = self.contract.events.EmitInvidualContestant().processReceipt(wait_for_complettion)
        self.assertTrue(event_filter[0]['args'].name == self.contestants)
        self.assertTrue(event_filter[0]['args'].ward == self.ward)
        self.assertTrue(event_filter[0]['args'].vote_count != 0)
        print("Vote for contestant Passed")

    def test_006_announceWinner(self):
        #Function only assume there is one user
        announceWinner = self.contract.functions.announceWinner().call()
        self.assertTrue(announceWinner[0] == self.contestants)
        self.assertTrue(announceWinner[1] == self.ward) 
        print("announceWinner Passed")


if __name__=="__main__":
    unittest.main()