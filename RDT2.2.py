# IMPLEMENTATION OF RDT 2.2 PROTOCOL

import random

class NetworkChannel:
    """A class representing an unreliable network channel with configurable error probability."""
    
    def __init__(self, error_rate=0.2):
        self.error_rate = error_rate
    
    def transmit(self, message):
        """Transmit a message through the unreliable channel, possibly corrupting it."""
        if random.random() < self.error_rate:
            valid_positions = [i for i, char in enumerate(message) if char != '|']
            position = random.choice(valid_positions)
            
            message_chars = list(message)
            message_chars[position] = chr((ord(message_chars[position]) + 1) % 128)
            return ''.join(message_chars)
        return message
    
    def transmit_acknowledgment(self, ack, error_rate=0.3):
        """Transmit an acknowledgment with possible loss."""
        return ack ^ 1 if random.random() < error_rate else ack


def convert_to_bytes(data):
    """Convert various data types to bytes for checksum calculation."""
    if isinstance(data, int):
        return data.to_bytes(4, byteorder='big')
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, bytes):
        return data
    else:
        raise TypeError("Unsupported data type for checksum calculation")


def calculate_integrity_check(sequence_number, payload):
    """Calculate an integrity check value for the given sequence number and payload."""
    seq_bytes = sequence_number.to_bytes(1, byteorder='big')
    payload_bytes = convert_to_bytes(payload)
    combined_bytes = seq_bytes + payload_bytes
    
    checksum_value = 0
    for byte in combined_bytes:
        checksum_value += byte
        checksum_value = (checksum_value & 0xFF) + (checksum_value >> 8) 
    
    return ~checksum_value & 0xFF


class DataSegment:
    """A class representing a data segment with sequence number, payload, and integrity check."""
    
    def __init__(self, sequence_number, payload):
        self.sequence_number = sequence_number
        self.payload = payload
        self.checksum = calculate_integrity_check(sequence_number, payload)
    
    def serialize(self):
        """Convert the segment to a string representation."""
        return f"{self.sequence_number}|{self.payload}|{self.checksum}"
    
    @staticmethod
    def deserialize(segment_string):
        """Create a segment from its string representation."""
        try:
            parts = segment_string.split('|')
            sequence_number = int(parts[0])
            payload = parts[1]
            received_checksum = int(parts[2])
            
            segment = DataSegment(sequence_number, payload)
            segment.checksum = received_checksum  
            return segment
        except Exception as e:
            print(f"Error parsing segment: {e}")
            return None


class TransmitterNode:
    """A class representing the sending endpoint in reliable data transfer."""
    
    def __init__(self):
        self.sequence_number = 0
    
    def transmit(self, payload, receiver, channel):
        """Send data to the receiver with reliability guarantees."""
        segment = DataSegment(self.sequence_number, payload)
        acknowledgment_received = False
        
        while not acknowledgment_received:
            transmitted_segment = channel.transmit(segment.serialize())
            print(f"Transmitter: Sending segment with payload: {segment.payload}, sequence number: {self.sequence_number}\n")
            
            acknowledgment = channel.transmit_acknowledgment(receiver.process_segment(transmitted_segment))
            print(f"Received acknowledgment: {acknowledgment}")
            
            if acknowledgment is not None and acknowledgment == self.sequence_number:
                self.sequence_number = self.sequence_number ^ 1
                acknowledgment_received = True
            else:
                print(f"Transmitter: Retransmitting...\n")


class ReceiverNode:
    """A class representing the receiving endpoint in reliable data transfer."""
    
    def __init__(self):
        self.expected_sequence_number = 0
    
    def process_segment(self, segment_string):
        """Process a received segment and return appropriate acknowledgment."""
        segment = DataSegment.deserialize(segment_string)
        
        if segment is None:
            print(f"Receiver: Segment received is corrupted, sending a dupplicate ACK: {self.expected_sequence_number ^ 1}\n")
            return self.expected_sequence_number ^ 1
        
        calculated_checksum = calculate_integrity_check(segment.sequence_number, segment.payload)
        
        if calculated_checksum != segment.checksum:
            print(f"Receiver: Checksum mismatch, sending a duplicate ACK: {self.expected_sequence_number ^ 1}\n")
            return self.expected_sequence_number ^ 1
        
        if segment.sequence_number == self.expected_sequence_number:
            print(f"Receiver: Correct segment, payload: {segment.payload}, transmitting data to the application layer, sending ACK: {segment.sequence_number}\n")
            self.expected_sequence_number ^= 1 
            return segment.sequence_number
        else:
            print(f"Receiver: Duplicate segment received, resending ACK: {self.expected_sequence_number ^ 1}\n")
            return self.expected_sequence_number ^ 1


if __name__ == "__main__":
    transmitter = TransmitterNode()
    receiver = ReceiverNode()
    channel = NetworkChannel(error_rate=0.2)

    messages = []
    print("Enter your messages and enter done to stop \n")
    
    while True:
        user_input = input("Enter the message:\n")
        if user_input.lower() == "done":
            break
        messages.append(user_input)
    
    print("\n")
    
    for message in messages:
        transmitter.transmit(message, receiver, channel)