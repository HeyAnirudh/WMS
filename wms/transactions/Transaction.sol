// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Transaction {
    uint256 public timestamp;
    address public currentId;
    address public nextId;
    uint256 public quantity;
    uint256 public quality;
    address[] public usersTransacted;

    event TransactionSent(
        uint256 timestamp,
        address indexed currentId,
        address indexed receiverId,
        uint256 indexed quantity,
        uint256 quality
    );
    event TransactionReceived(
        uint256 indexed timestamp,
        address indexed currentId,
        address indexed receiverId,
        uint256 quantity,
        uint256 quality
    );

    function createTransaction(
        address senderId,
        address receiverId,
        uint256 _quantity,
        uint256 _quality
    ) public {
        timestamp = block.timestamp;
        currentId = senderId;
        nextId = receiverId;
        quality = _quality;
        quantity = _quantity;

        usersTransacted.push(senderId);
        emit TransactionSent(
            timestamp,
            senderId,
            receiverId,
            _quantity,
            _quality
        );
    }
}
