// contracts/customToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable{

    address[] public allowedTokens;
    address[] public stakers;
    IERC20 public dappToken;
    mapping(address => mapping(address => uint256)) public stakingBalance;
    mapping(address => uint256) public uniqueTokensStaked;
    mapping(address => address) public tokenPriceFeedMap;

    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }





    function issueTokens() public onlyOwner{
        for (uint256 stakersIndex = 0; stakersIndex < stakers.length; stakersIndex++){
            address recipient = stakers[stakersIndex];
            dappToken.transfer(recipient, getUserTotalValue(recipient));

        }
       
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No tokens staked");
        for(uint256 allowedTokensIndex = 0 ; allowedTokensIndex < allowedTokens.length; allowedTokensIndex++){
            totalValue = totalValue + getUserSingleTokenValue(_user,allowedTokens[allowedTokensIndex]);
        }

        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token) public view returns (uint256){

        if(uniqueTokensStaked[_user] <= 0){
            return 0;
        }
        (uint256 _price, uint256 _decimals) = getTokenValue(_token);

        return (stakingBalance[_token][_user] * _price / (10**_decimals));

    }

    function getTokenValue(address _token) public view returns (uint256, uint256){

        address priceFeedAddress = tokenPriceFeedMap[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,,) = priceFeed.latestRoundData();
        uint8 decimals = priceFeed.decimals();
        
        return (uint256(price), uint256(decimals));
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner{
        tokenPriceFeedMap[_token] = _priceFeed;
    }

    function updateuniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] == 0){
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be higher than 0");
        require(isTokenAllowed(_token), "Token is not allowed");
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateuniqueTokensStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] = stakingBalance[_token][msg.sender] + _amount;
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unStakeTokens(address _token) public {

        uint256 balance = stakingBalance[_token][msg.sender];
        require (balance > 0, "Staking Balance cannot be 0");

        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;

        uniqueTokensStaked[msg.sender]--;
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function isTokenAllowed(address _token) public returns (bool) {
        for(uint256 allowedTokensIt = 0; allowedTokensIt < allowedTokens.length; allowedTokensIt++) {
            if (allowedTokens[allowedTokensIt] == _token) return true;
        }
        return false;
    }
}