// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;



contract VotingContract{

    uint createdTime;

    struct voters {
        bool voted;
        address user_address;
    }
    mapping(address => voters) IndividualVoter;

    struct Contestant {
        string name;
        string ward; // Where they represent
        uint vote_count;

    }
    mapping(string => Contestant) IndividualContestant;
    string[] ContestantList;


    event EmitContestant (
        string name,
        string ward, // Where they represent
        uint vote_count
    );

    event EmitInvidualContestant(
        string name,
        string ward, // Where they represent
        uint vote_count
    );
    

    event contesterAdded(
        string name,
        string ward,
        uint vote_count
    );


    /** Add Contestant to Blockchain, checks to make sure total users not more than 5 and Checks if contestant has been added before */
    constructor() public {
        createdTime = block.timestamp;
    }

    function AddContestant(string memory _name, string memory _ward ) public {
            Contestant memory _contestant = IndividualContestant[_name];
            bytes memory _check_contestLen = bytes(_contestant.name);
            uint total_Acceptable_con = 5; //Total number of allowed contestant, this can be made a state variable

            if (_check_contestLen.length == 0) {
                if (ContestantList.length < total_Acceptable_con) {
                _contestant.name = _name;
                _contestant.ward = _ward;
                _contestant.vote_count = 0;
                IndividualContestant[_name] = _contestant;
                ContestantList.push(_name);
                emit contesterAdded(_contestant.name, _contestant.ward, _contestant.vote_count);
                } else if (ContestantList.length >= total_Acceptable_con){
                    revert("Max Candidate Reached");
                }

            } else if (_check_contestLen.length != 0){
                revert("Contestant Already added");
            }

    }

    /** Get list of all Contestant from BlockChain */

    function getContestants() public {
        for(uint i =0; i<ContestantList.length; i++) {
            Contestant memory  _current_contestant = IndividualContestant[ContestantList[i]];
            emit EmitContestant(_current_contestant.name, _current_contestant.ward, _current_contestant.vote_count);
        }

    }
    /** Get Individuals Contestant from all lis and return all their attributes */

    function getIndividualContestant(string memory _con_name) public {
        Contestant memory _current_contestant = IndividualContestant[_con_name];
        emit EmitInvidualContestant(_current_contestant.name, _current_contestant.ward, _current_contestant.vote_count);


    }
    /** Function to cast vote for contest, checks to make sure users dont vote twice */
    function CastVote(string memory _name) public {
        // require(block.timestamp >= createdTime + 30);
        voters storage _current_voter = IndividualVoter[msg.sender];
        if (_current_voter.voted == true){
            revert("You Already Voted");
        } else if(_current_voter.voted != true){
            Contestant storage Voter_contestant = IndividualContestant[_name];
            Voter_contestant.vote_count +=1;
            _current_voter.voted = true;
            emit EmitInvidualContestant(Voter_contestant.name, Voter_contestant.ward, Voter_contestant.vote_count);
        }

    }

    function announceWinner() public view returns(string memory, string memory, uint){
        uint WinnerCount = 0;
        string memory winner_name;
        for(uint i =0; i<ContestantList.length; i++) {
            Contestant memory winner =  IndividualContestant[ ContestantList[i] ];
            if( winner.vote_count > WinnerCount){
                WinnerCount = winner.vote_count;
                winner_name = winner.name;
            }
    }
    
        return(IndividualContestant[winner_name].name, IndividualContestant[winner_name].ward, IndividualContestant[winner_name].vote_count);

}
}